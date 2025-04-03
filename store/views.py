from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.db.models import Q

def home(request):
    # Get parent categories only for the main navigation
    parent_categories = Category.objects.filter(parent=None)
    
    # Get featured products
    featured_products = Product.objects.filter(available=True)[:8]
    
    # Get categories marked as featured
    featured_categories = Category.objects.filter(is_featured=True)[:4]
    
    # Get newest products
    new_products = Product.objects.filter(available=True).order_by('-created')[:4]
    
    return render(request, 'store/home.html', {
        'parent_categories': parent_categories,
        'featured_categories': featured_categories,
        'featured_products': featured_products,
        'new_products': new_products,
    })

def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Filter bestsellers
    if request.GET.get('bestseller'):
        # Assuming you have a bestseller field or can determine this somehow
        products = products.filter(bestseller=True)
    
    # Filter new products
    if request.GET.get('new'):
        # Get products from the last 30 days
        from datetime import timedelta
        from django.utils import timezone
        thirty_days_ago = timezone.now() - timedelta(days=30)
        products = products.filter(created__gte=thirty_days_ago)
    
    # Filter discounted products
    if request.GET.get('discount'):
        # Assuming you have a way to track discounted products
        products = products.filter(discount__gt=0)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    # Sort products
    sort = request.GET.get('sort')
    if sort:
        products = products.order_by(sort)
    else:
        products = products.order_by('name')
    
    return render(request, 'store/product/list.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, id, slug=None):
    product = get_object_or_404(Product, id=id, available=True)
    
    return render(request, 'store/product/detail.html', {
        'product': product
    })