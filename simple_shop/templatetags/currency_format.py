from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='rupiah')
def rupiah(value):
    try:
        value = float(value)
        return f"Rp {value:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
    except (ValueError, TypeError):
        return ""
