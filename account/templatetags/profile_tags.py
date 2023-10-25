from django import template

from receips.models import Receipe
from account.models import Profile

register = template.Library()


@register.simple_tag
def get_recipes_count(auth_pk) -> int:
    return Receipe.objects.select_related("author").filter(author__pk=auth_pk).count()


@register.simple_tag
def get_profile(auth_pk):
    print("-------------")
    print(Profile.objects.filter(user__pk=auth_pk).first())
    return Profile.objects.filter(user__pk=auth_pk).first()
