from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city', 
        'payment_status', 'order_status', 'modified',
        'created'
    ]
    list_filter = [
        'payment_status', 'order_status', 'modified',
        'created'
    ]
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email', 'address']
    list_per_page = 20
    date_hierarchy = 'created'
