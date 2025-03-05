from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='rupiah_format')
def rupiah_format(value):
    try:
        value = float(value)
        return f"Rp{value:,.2f}".replace(',', '.')
    except:
        return value
