from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='rupiah')
def rupiah(value):
    try:
        value = float(value)
        return f"Rp {value:,.0f}".replace(',', '@').replace('.', ',').replace('@', '.')
    except (ValueError, TypeError):
        return ''
