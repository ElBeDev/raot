from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Category, SiteCustomization

# Custom ModelAdmin classes
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'available', 'image_preview']
    # Change or remove the created_at field that's causing the error
    list_filter = ['available', 'category']  # Remove 'created_at'
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "No Image"
    
    image_preview.short_description = 'Preview'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

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

# Register with the default admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
