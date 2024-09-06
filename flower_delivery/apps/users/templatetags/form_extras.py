from django import template

register = template.Library()


@register.filter
def add_class(value, arg):
    return value.as_widget(attrs={"class": arg})


@register.filter
def mul(value, arg):
    return value * arg


@register.filter
def star_rating(value):
    full_stars = int(value)
    empty_stars = 5 - full_stars
    return "★" * full_stars + "☆" * empty_stars
