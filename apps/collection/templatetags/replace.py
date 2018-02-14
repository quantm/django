#__author__ = 'tqn'
from django import template


register = template.Library()

@register.filter
def replace(string, args):
    args = args.split(':')
    search  = args[0]
    replace = args[1]

    return string.replace(search, replace)