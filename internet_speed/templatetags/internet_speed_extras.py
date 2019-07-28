from django import template

register = template.Library()

@register.filter
def tofloat(value):
    return float(value)


