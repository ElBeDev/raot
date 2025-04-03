from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.conf import settings
from .clipmx import ClipMX
from .email import send_order_confirmation, send_payment_confirmation

def order_create(request):
    cart = Cart(request)
    
    # If cart is empty, redirect to cart page
    if len(cart) == 0:
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Clear the cart
            cart.clear()
            
            # Store the order ID in the session
            request.session['order_id'] = str(order.id)
            
            # Send order confirmation email
            send_order_confirmation(order)
            
            # Redirect to payment page
            return redirect(reverse('checkout:payment'))
    else:
        form = OrderCreateForm()
    
    return render(request, 'checkout/create.html', {'cart': cart, 'form': form})

def payment_process(request):
    # Get order ID from session
    order_id = request.session.get('order_id')
    
    if not order_id:
        return redirect('store:product_list')
        
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Initialize CLIP.MX
        clipmx = ClipMX()
        
        # Generate the return URL
        return_url = request.build_absolute_uri(reverse('checkout:payment_completed'))
        
        # Create payment in CLIP.MX
        result = clipmx.create_payment(order, return_url)
        
        if result['success']:
            # Store payment ID in the order
            order.payment_id = result['payment_id']
            order.save()
            
            # Redirect to CLIP.MX payment page
            return redirect(result['payment_url'])
        else:
            # Handle payment creation error
            return render(request, 'checkout/payment.html', {
                'order': order,
                'error': result.get('error', 'Payment processing failed.')
            })
    
    # Display payment form
    return render(request, 'checkout/payment.html', {'order': order})

def payment_completed(request):
    # Get order ID from session
    order_id = request.session.get('order_id')
    payment_id = request.GET.get('payment_id')
    
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        
        if payment_id:
            # Verify payment status
            clipmx = ClipMX()
            result = clipmx.verify_payment(payment_id)
            
            if result['success'] and result['data'].get('status') == 'successful':
                # Mark order as paid
                order.paid = True
                order.payment_status = 'completed'
                order.payment_date = timezone.now()
                order.save()
                
                # Send payment confirmation email
                send_payment_confirmation(order)
            
        return render(request, 'checkout/completed.html', {'order': order})
    
    return redirect('store:product_list')

@csrf_exempt
def payment_webhook(request):
    """Handle CLIP.MX webhook notifications"""
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    # Get webhook signature from headers
    signature = request.headers.get('Clip-Signature', '')
    
    # Process the webhook data
    clipmx = ClipMX()
    result = clipmx.process_webhook(request.body.decode('utf-8'), signature)
    
    if result['success'] and result.get('status') == 'paid':
        try:
            # Update order status
            order = Order.objects.get(id=result['order_id'])
            order.paid = True
            order.payment_status = 'completed'
            order.payment_date = timezone.now()
            order.save()
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
    
    return JsonResponse({'status': 'success'})

def order_tracking(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'checkout/tracking.html', {'order': order})
