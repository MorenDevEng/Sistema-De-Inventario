from django import template

register = template.Library()

@register.filter
def multiplicar(value, arg):
    """Multiplica los valores dados"""

    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''