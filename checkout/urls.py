from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('tracking/<uuid:order_id>/', views.order_tracking, name='order_tracking'),
    path('webhook/clip/', views.clip_webhook, name='clip_webhook'),
    path('test_or_real/<uuid:order_id>/', views.test_or_real, name='test_or_real'),
]