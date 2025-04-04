from django.db import models
from django.utils.translation import gettext_lazy as _
from store.models import Product
import uuid

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de creación'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('Última actualización'))
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    
    ORDER_STATUS_CHOICES = (
        ('created', _('Creado')),
        ('processing', _('Procesando')),
        ('shipped', _('Enviado')),
        ('delivered', _('Entregado')),
        ('cancelled', _('Cancelado')),
    )
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='created',
        verbose_name=_('Estado del Pedido')
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('card', _('Tarjeta de crédito/débito')),
        ('oxxo', _('OXXO')),
        ('transfer', _('Transferencia bancaria')),
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='card',
        verbose_name=_('Método de Pago')
    )
    
    payment_date = models.DateTimeField(blank=True, null=True)
    shipping_tracking_code = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name=_('Código de Seguimiento')
    )
    shipping_tracking_url = models.URLField(
        blank=True, 
        verbose_name=_('URL de Seguimiento')
    )
    shipping_company = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name=_('Empresa de Envío')
    )
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        """Calculate the total cost of the order"""
        return sum(item.get_cost() for item in self.items.all())
    
    def get_tracking_link(self):
        return f"/order-tracking/{self.id}/"
    
    def generate_reference(self):
        return f"RAOT-{self.id}-{uuid.uuid4().hex[:6].upper()}"
    
    def get_order_status_display(self):
        """Get the display name for the order status"""
        status_choices = dict(self._meta.get_field('order_status').choices)
        return status_choices.get(self.order_status, self.order_status)
    
    def get_payment_status_display(self):
        """Get the display name for the payment status"""
        status_choices = dict(self._meta.get_field('payment_status').choices)
        return status_choices.get(self.payment_status, self.payment_status)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        """Calculate the cost of this order item"""
        return self.price * self.quantity
