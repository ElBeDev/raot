from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation(order):
    """
    Send order confirmation email to the customer
    """
    subject = f'RAOT Order Confirmation - Order #{order.id}'
    
    message = render_to_string('checkout/emails/order_confirmation.txt', {
        'order': order,
        'tracking_url': f"{settings.SITE_URL}/checkout/tracking/{order.id}/"
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False
    )

def send_payment_confirmation(order):
    """
    Send payment confirmation email to the customer
    """
    subject = f'RAOT Payment Confirmation - Order #{order.id}'
    
    message = render_to_string('checkout/emails/payment_confirmation.txt', {
        'order': order,
        'tracking_url': f"{settings.SITE_URL}/checkout/tracking/{order.id}/"
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False
    )