from django import template

register = template.Library()


@register.simple_tag()
def row_number(a, b, forloop_counter):
    return (a - 1) * b + forloop_counter
