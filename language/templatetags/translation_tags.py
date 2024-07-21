from django import template
from ..utils import get_translation

register = template.Library()

@register.simple_tag(takes_context=True)
def translate(context, key):
    request = context['request']
    return get_translation(key, request)
