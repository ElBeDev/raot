from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories', blank=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])

# Admin dashboard widget
class RecentProductsWidget:
    """Display recent products in the admin dashboard."""
    template = 'admin/recent_products_widget.html'
    
    def __init__(self, request):
        self.request = request
    
    def get_context(self):
        return {
            'title': 'Recently Added Products',
            'products': Product.objects.all().order_by('-created_at')[:5],
            'user': self.request.user,
        }

class SiteCustomization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    css_content = models.TextField(blank=True, help_text="Custom CSS to apply to the site")
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Site Customization"
        verbose_name_plural = "Site Customizations"
