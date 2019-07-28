from django import template

register = template.Library()

@register.filter
def tofloat(value):
    if value == -1:
        return 'N/A'
    return float(value)


