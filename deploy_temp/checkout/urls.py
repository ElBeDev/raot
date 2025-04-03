from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/', views.payment_process, name='payment'),
    path('completed/', views.payment_completed, name='completed'),
    path('tracking/<uuid:order_id>/', views.order_tracking, name='order_tracking'),
    path('webhook/', views.payment_webhook, name='webhook'),
]