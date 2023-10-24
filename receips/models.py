from collections.abc import Iterable
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify
from unidecode import unidecode
from taggit.managers import TaggableManager


class Category(models.Model):
    title = models.CharField(max_length=128, verbose_name="Категория")
    slug = models.SlugField(max_length=128, unique=True, db_index=True)
    image = models.ImageField(
        upload_to="images/category/", blank=True, verbose_name="Изображение категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Receipe(models.Model):
    title = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, unique=True, verbose_name="url")
    description = models.TextField(verbose_name="Описание рецепта")
    cooking_steps = models.TextField(verbose_name="Инструкция")
    ingredient = models.TextField(verbose_name="Ингредиенты ")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления (мин.)",
    )
    servings = models.PositiveSmallIntegerField(verbose_name="Количество порций")
    image = models.ImageField(
        upload_to="images/%Y/%m/%d/", blank=True, verbose_name="Фото"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="receipes",
        verbose_name="Автор",
        on_delete=models.PROTECT,
    )
    category = models.ForeignKey(
        Category,
        related_name="receipes",
        on_delete=models.PROTECT,
        verbose_name="Категория",
    )
    tags = TaggableManager(verbose_name="Теги", help_text="Список тегов", blank=True)
    user_likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="likes", blank=True
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Опубликован")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def __str__(self) -> str:
        return f"{self.title} - {self.author.username}"

    def get_absolute_url(self):
        return reverse("receips:receipe_detail", kwargs={"rec_slug": self.slug})

    def save(self, *args, **kwargs) -> None:
        title = unidecode(self.title)
        self.slug = slugify(title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]
