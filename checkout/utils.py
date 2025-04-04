from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order):
    """Send order confirmation email to the customer"""
    subject = f'RAOT Suplementos - Confirmación de Pedido #{order.id}'
    
    # Context for the email template
    context = {
        'order': order,
        'site_name': 'RAOT Suplementos',
        'site_url': settings.SITE_URL,
    }
    
    # Render the HTML email template
    html_message = render_to_string('checkout/email/order_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    # Get sender email from settings
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@raotsuplementos.com.mx')
    
    # Get recipient email from order
    to_email = order.email
    
    # Send the email
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_message,
            fail_silently=False
        )
        logger.info(f"Order confirmation email sent to {to_email} for order #{order.id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send order confirmation email: {str(e)}")
        raise