from django import template

register = template.Library()

@register.filter
def currency_posneg(value):
    try:
        value = float(value)
        if value < 0:
            return "-${:,.2f}".format(abs(value))
        else:
            return "${:,.2f}".format(value)
    except:
        return value
