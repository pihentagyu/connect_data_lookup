from django import template

register = template.Library()

@register.filter
def tofloat(value):
    '''Converts fixed to float. If value is -1, returns N/A'''
    if value == -1:
        return 'N/A'
    return float(value)


