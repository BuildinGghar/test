from django import template

register = template.Library()

@register.filter(name='ends_with')
def ends_with(value, ending):
    return value.lower().endswith(ending.lower())
