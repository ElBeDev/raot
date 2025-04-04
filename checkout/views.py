from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
import json
import hmac
import hashlib
import logging
import uuid

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .clip_payment import ClipPaymentGateway
from .emails import send_order_confirmation_email
from .utils import send_order_confirmation_email

# Set up logging
logger = logging.getLogger(__name__)

def order_create(request):
    cart = Cart(request)
    
    # Check if cart is empty
    if not cart:
        messages.warning(request, 'Tu carrito está vacío. Por favor, añade algunos productos antes de realizar el pedido.')
        return redirect('store:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            # Set default values for payment fields
            order.payment_status = 'pending'
            order.order_status = 'pending'
            
            # If user is authenticated, associate order with user
            if request.user.is_authenticated:
                order.user = request.user
            
            # Save the order
            order.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear the cart
            cart.clear()
            
            # Store order ID in session (as a string, not a UUID)
            request.session['order_id'] = str(order.id)  # Convert UUID to string
            
            # Redirect to payment page
            return redirect(reverse('checkout:payment_process'))
    else:
        form = OrderCreateForm()
    
    return render(request, 'checkout/create.html', {
        'cart': cart,
        'form': form
    })

def payment_process(request):
    # Get the order ID from the session
    order_id = request.session.get('order_id')
    if not order_id:
        # If no order ID in session, redirect to product list
        messages.error(request, 'No se encontró ningún pedido para procesar el pago.')
        return redirect('store:product_list')
    
    # Get the order object
    order = get_object_or_404(Order, id=order_id)
    
    # Initialize the CLIP.MX payment gateway
    clip = ClipPaymentGateway()
    
    # Create a payment link
    result = clip.create_payment_link(order)
    
    if not result['success']:
        # If payment link creation failed, show error
        messages.error(request, f"Error al crear enlace de pago: {result.get('error', 'Error desconocido')}")
        return redirect('checkout:order_create')
    
    # Redirect to the payment page
    return redirect(result['payment_url'])

def payment_success(request):
    # Get the order ID from query parameters
    order_id = request.GET.get('order_id')
    if not order_id:
        messages.error(request, 'No se encontró información del pedido.')
        return redirect('store:product_list')
    
    # Get the order
    order = get_object_or_404(Order, id=order_id)
    
    # Check if this is a simulated payment (fallback mode)
    payment_id = request.GET.get('payment_id')
    if payment_id and payment_id.startswith('sim_payment_'):
        # This is a simulated payment - mark as paid
        order.payment_status = 'paid'
        order.order_status = 'processing'
        order.transaction_id = payment_id
        order.save()
        
        # Clear the cart
        cart = Cart(request)
        cart.clear()
        
        # Try to send confirmation email
        try:
            send_order_confirmation_email(order)
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {str(e)}")
        
        messages.success(request, 'Pago simulado exitoso (modo de desarrollo).')
    
    # For real payments, verify with CLIP.MX if not already marked as paid
    elif order.payment_status != 'paid':
        # Verify payment status with CLIP.MX
        clip = ClipPaymentGateway()
        
        try:
            result = clip.verify_payment(order.payment_id)
            
            if result['success'] and result.get('status') == 'paid':
                # Update order status
                order.payment_status = 'paid'
                order.order_status = 'processing'
                if result.get('transaction_id'):
                    order.transaction_id = result.get('transaction_id')
                order.save()
                
                # Clear the cart
                cart = Cart(request)
                cart.clear()
                
                # Send confirmation email
                try:
                    send_order_confirmation_email(order)
                except Exception as e:
                    logger.error(f"Failed to send confirmation email: {str(e)}")
        except Exception as e:
            logger.error(f"Error verifying payment: {str(e)}")
            # Still show the success page even if verification fails
    
    # Render success page
    return render(request, 'checkout/payment_success.html', {
        'order': order
    })

def payment_cancel(request):
    # Get the order ID from query parameters
    order_id = request.GET.get('order_id')
    if not order_id:
        messages.error(request, 'No se encontró información del pedido.')
        return redirect('store:product_list')
    
    # Get the order
    order = get_object_or_404(Order, id=order_id)
    
    # Update order status
    order.payment_status = 'cancelled'
    order.save(update_fields=['payment_status'])
    
    # Render cancel page
    return render(request, 'checkout/payment_cancel.html', {
        'order': order
    })

@csrf_exempt
@require_POST
def clip_webhook(request):
    """
    Webhook handler for CLIP.MX payment events
    
    This endpoint receives notifications from CLIP.MX when:
    - Payment is completed
    - Payment fails
    - Refund is processed
    """
    # Get the webhook payload and signature
    payload = request.body
    signature = request.headers.get('Clip-Signature')
    
    # Log webhook receipt
    logger.info(f"Received webhook from CLIP.MX: {request.headers.get('X-Clip-Event', 'unknown-event')}")
    
    # Verify signature
    if not signature:
        logger.warning("Received webhook without signature")
        return HttpResponse(status=400)
    
    # Verify webhook signature
    try:
        webhook_secret = getattr(settings, 'CLIP_WEBHOOK_SECRET', settings.CLIP_SECRET_KEY)
        expected_signature = hmac.new(
            key=webhook_secret.encode(),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected_signature, signature):
            logger.warning("Invalid webhook signature")
            return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"Error verifying webhook signature: {str(e)}")
        return HttpResponse(status=400)
    
    # Parse the payload
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in webhook payload")
        return HttpResponse(status=400)
    
    # Get event type and payment details
    event_type = data.get('type')
    payment_data = data.get('data', {})
    payment_id = payment_data.get('id')
    
    # Log webhook event details
    logger.info(f"Processing CLIP.MX webhook: {event_type} for payment {payment_id}")
    
    # Handle different event types
    if event_type == 'payment.completed' or event_type == 'payment.succeeded':
        # Payment was successful
        try:
            # Try to find order by payment ID
            order = Order.objects.get(payment_id=payment_id)
            
            # Avoid duplicate processing
            if order.payment_status == 'paid':
                logger.info(f"Order {order.id} already marked as paid, skipping")
                return HttpResponse(status=200)
            
            # Update order status
            order.payment_status = 'paid'
            order.order_status = 'processing'
            if payment_data.get('transaction_id'):
                order.transaction_id = payment_data.get('transaction_id')
            order.save()
            
            logger.info(f"Successfully marked order {order.id} as paid")
            
            # Send confirmation email
            try:
                send_order_confirmation_email(order)
                logger.info(f"Sent confirmation email for order {order.id}")
            except Exception as e:
                logger.error(f"Failed to send order confirmation email: {str(e)} - Order ID: {order.id}")
            
            return HttpResponse(status=200)
            
        except Order.DoesNotExist:
            logger.error(f"Order not found for payment ID: {payment_id}")
            return HttpResponse(status=404)
            
        except Exception as e:
            logger.error(f"Error processing payment.completed webhook: {str(e)}")
            return HttpResponse(status=500)
    
    elif event_type == 'payment.failed':
        # Payment failed
        try:
            order = Order.objects.get(payment_id=payment_id)
            
            # Update order status
            order.payment_status = 'failed'
            order.save(update_fields=['payment_status'])
            
            logger.info(f"Marked order {order.id} as failed payment")
            return HttpResponse(status=200)
        except Order.DoesNotExist:
            logger.error(f"Order not found for payment ID: {payment_id}")
            return HttpResponse(status=404)
        except Exception as e:
            logger.error(f"Error processing payment.failed webhook: {str(e)}")
            return HttpResponse(status=500)
    
    elif event_type == 'refund.completed':
        # Refund was processed
        try:
            order = Order.objects.get(payment_id=payment_id)
            
            # Update order status
            order.payment_status = 'refunded'
            order.save(update_fields=['payment_status'])
            
            logger.info(f"Marked order {order.id} as refunded")
            return HttpResponse(status=200)
        except Order.DoesNotExist:
            logger.error(f"Order not found for payment ID: {payment_id}")
            return HttpResponse(status=404)
        except Exception as e:
            logger.error(f"Error processing refund.completed webhook: {str(e)}")
            return HttpResponse(status=500)
    
    # For other event types, just acknowledge receipt
    logger.info(f"Received unhandled event type: {event_type}")
    return HttpResponse(status=200)

def order_tracking(request, order_id):
    """
    View to allow customers to track their order status
    """
    try:
        # Try to fetch the order with the given ID
        order = get_object_or_404(Order, id=order_id)
        
        # Check if email verification is required (optional security measure)
        email = request.GET.get('email')
        if email and email != order.email:
            messages.error(request, 'El correo electrónico proporcionado no coincide con el pedido.')
            return render(request, 'checkout/tracking_error.html')
        
        # Get order items
        items = order.items.all()
        
        # Render the tracking template with order details
        return render(request, 'checkout/tracking.html', {
            'order': order,
            'items': items,
        })
    
    except Exception as e:
        # Log the error
        logger.error(f"Error in order tracking: {str(e)}")
        messages.error(request, 'Hubo un problema al recuperar la información del pedido.')
        return render(request, 'checkout/tracking_error.html')

def test_or_real(request, order_id):
    """
    Page that allows choosing between simulated payment and real CLIP payment
    """
    # Get the order
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        choice = request.POST.get('choice')
        
        if choice == 'real':
            # User wants to try real CLIP payment
            # Create a direct request to CLIP.MX API
            clip = ClipPaymentGateway()
            
            try:
                # Force API call to CLIP.MX without fallback
                result = clip._direct_api_call(order)
                
                if result['success']:
                    # Redirect to the real payment URL
                    return redirect(result['payment_url'])
                else:
                    # Show error and offer fallback
                    messages.error(request, f"Error al conectar con CLIP.MX: {result.get('error', 'Error desconocido')}")
                    return render(request, 'checkout/test_or_real.html', {
                        'order': order,
                        'api_error': result.get('error')
                    })
            except Exception as e:
                # Show connection error
                messages.error(request, f"Error de conexión: {str(e)}")
                return render(request, 'checkout/test_or_real.html', {
                    'order': order,
                    'api_error': str(e)
                })
        
        elif choice == 'simulate':
            # User wants to simulate payment
            # Generate simulated payment ID if not exists
            if not order.payment_id or not order.payment_id.startswith('sim_payment_'):
                order.payment_id = f"sim_payment_{uuid.uuid4().hex[:10]}"
                order.save(update_fields=['payment_id'])
            
            # Redirect to payment success with simulated ID
            return redirect(reverse('checkout:payment_success') + f'?order_id={order.id}&payment_id={order.payment_id}')
    
    # Render the choice page
    return render(request, 'checkout/test_or_real.html', {
        'order': order
    })
