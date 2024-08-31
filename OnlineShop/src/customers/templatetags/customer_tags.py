from django import template

register = template.Library()

from website.models import Ratings

@register.simple_tag
def customer_rate(product_obj, customer_id):
    return Ratings.get_product_rate(product_obj, customer_id)