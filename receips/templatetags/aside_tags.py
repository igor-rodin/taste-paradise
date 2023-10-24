from django import template
from taggit.models import Tag

from receips.models import Category

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.all()
