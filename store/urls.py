from django.urls import path, re_path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('products/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]