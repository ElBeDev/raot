from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Category, SiteCustomization

# Custom ModelAdmin classes
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug', 'display_order', 'is_featured']
    list_filter = ['is_featured', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['display_order', 'is_featured']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'available', 'image_preview']
    list_filter = ['available', 'category']  # Remove 'created_at'
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "No Image"
    
    image_preview.short_description = 'Preview'

@admin.register(SiteCustomization)
class SiteCustomizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_updated')
    search_fields = ('name',)
    
    class Media:
        css = {
            'all': ('vendor/codemirror/lib/codemirror.css',)
        }
        js = (
            'vendor/codemirror/lib/codemirror.js',
            'vendor/codemirror/mode/css/css.js',
            'js/admin_css_editor.js',
        )
