from django.contrib import admin

from receips.models import Receipe, Category
from .forms import ReceipeForm


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Receipe)
class AdminReceipe(admin.ModelAdmin):
    # form = ReceipeForm

    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        "short_desc",
        "cooking_time",
        "category",
        "author",
        "tag_list",
    )

    fields = (
        "title",
        "image",
        "description",
        "cooking_steps",
        "ingredient",
        "cooking_time",
        "servings",
        "category",
        "tags",
        "slug",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    @admin.display(description="Теги")
    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    @admin.display(description="Описание")
    def short_desc(self, obj):
        if len(obj.description) < 50:
            return obj.description
        return f"{obj.description[:50]}..."
