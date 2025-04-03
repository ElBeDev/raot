from django import template
from store.models import SiteCustomization

register = template.Library()

@register.simple_tag
def get_custom_css():
    try:
        custom_css = SiteCustomization.objects.first()
        if custom_css:
            return custom_css.css_content
    except Exception as e:
        print(f"Error loading custom CSS: {e}")
    return ""
