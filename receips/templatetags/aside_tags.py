from django import template
from taggit.models import Tag

from receips.models import Category, Receipe

register = template.Library()


@register.simple_tag
def get_categories():
    """
    Возвращает все категории рецептов
    """
    return Category.objects.all()


@register.simple_tag
def get_tags():
    """
    Возвращает все теги
    """
    return Tag.objects.all()


@register.simple_tag(name="user_receipes")
def get_user_receipes(user_pk: int):
    """
    Возвращает рецепты, добавленные конкретным пользоателем
    """
    print(Receipe.objects.select_related("author").filter(author__pk=user_pk).all())
    return Receipe.objects.select_related("author").filter(author__pk=user_pk).all()
