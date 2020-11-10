from django import template

register = template.Library()

@register.filter
def discount_amount(item):
    delta = 0
    try:
        delta = item.price - item.discounted_price
    except Exception:
        return delta
    return delta
