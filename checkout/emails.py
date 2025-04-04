from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)

def send_order_confirmation_email(order):
    """
    Send order confirmation email to customer after successful payment
    
    Args:
        order: The Order instance with customer and order details
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        subject = f'RAOT Suplementos - Confirmación de Pedido #{order.id}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = order.email
        
        # Prepare context for email templates
        context = {
            'order': order,
            'items': order.items.all(),
            'total_cost': order.get_total_cost(),
            'site_url': settings.SITE_URL,
        }
        
        # Render email content from templates
        html_message = render_to_string('checkout/emails/order_confirmation.html', context)
        plain_message = render_to_string('checkout/emails/order_confirmation_plain.html', context)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_message,
            fail_silently=False
        )
        
        # Log successful email sending
        logger.info(f"Order confirmation email sent to {to_email} for order #{order.id}")
        return True
        
    except Exception as e:
        # Log error but don't raise exception to avoid breaking the payment flow
        logger.error(f"Failed to send order confirmation email: {str(e)} - Order ID: {order.id}")
        return False

def send_shipping_notification(order):
    """
    Send shipping notification email to customer when order is shipped
    
    Args:
        order: The Order instance with shipping details
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        subject = f'RAOT Suplementos - Tu pedido #{order.id} ha sido enviado'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = order.email
        
        # Prepare context for email templates
        context = {
            'order': order,
            'tracking_code': order.shipping_tracking_code,
            'tracking_url': order.shipping_tracking_url,
            'shipping_company': order.shipping_company,
            'site_url': settings.SITE_URL,
        }
        
        # Render email content from templates
        html_message = render_to_string('checkout/emails/shipping_notification.html', context)
        plain_message = render_to_string('checkout/emails/shipping_notification_plain.html', context)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_message,
            fail_silently=False
        )
        
        # Log successful email sending
        logger.info(f"Shipping notification email sent to {to_email} for order #{order.id}")
        return True
        
    except Exception as e:
        # Log error
        logger.error(f"Failed to send shipping notification email: {str(e)} - Order ID: {order.id}")
        return False

def send_payment_failure_notification(order, error_message=None):
    """
    Send payment failure notification to customer
    
    Args:
        order: The Order instance
        error_message: Optional error message to include
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        subject = f'RAOT Suplementos - Problema con tu pago para el pedido #{order.id}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = order.email
        
        # Prepare context for email templates
        context = {
            'order': order,
            'error_message': error_message or 'Hubo un problema al procesar tu pago.',
            'site_url': settings.SITE_URL,
        }
        
        # Render email content from templates
        html_message = render_to_string('checkout/emails/payment_failure.html', context)
        plain_message = render_to_string('checkout/emails/payment_failure_plain.html', context)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_message,
            fail_silently=False
        )
        
        # Log successful email sending
        logger.info(f"Payment failure notification email sent to {to_email} for order #{order.id}")
        return True
        
    except Exception as e:
        # Log error
        logger.error(f"Failed to send payment failure notification email: {str(e)} - Order ID: {order.id}")
        return False