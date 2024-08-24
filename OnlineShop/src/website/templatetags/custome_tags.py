from django import template

register = template.Library()

@register.simple_tag
def numeric_loop(value):
    return range(1, int(value)+1)