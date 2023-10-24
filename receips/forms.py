from django import forms

from .models import Receipe, Category


class ReceipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="Выберите категорию...",
        widget=forms.Select(attrs={"class": "receipe__input"}),
    )

    # description = forms.CharField(widget=CKEditorUploadingWidget(), label="Описание")

    class Meta:
        model = Receipe
        fields = (
            "title",
            "category",
            "description",
            "cooking_steps",
            "ingredient",
            "cooking_time",
            "servings",
            "image",
            "tags",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "receipe__input",
                    "rows": 5,
                    "placeholder": "Название рецепта",
                }
            ),
            "cooking_time": forms.NumberInput(
                attrs={
                    "class": "receipe__input",
                    "value": "10",
                }
            ),
            "servings": forms.NumberInput(
                attrs={
                    "class": "receipe__input",
                    "value": "2",
                }
            ),
            "description": forms.Textarea(attrs={"class": "receipe__input", "rows": 5}),
            "cooking_steps": forms.Textarea(
                attrs={"class": "receipe__input", "rows": 5}
            ),
            "ingredient": forms.Textarea(attrs={"class": "receipe__input", "rows": 5}),
            "tags": forms.TextInput(
                attrs={
                    "class": "receipe__input",
                    "placeholder": "(Например: полезно мясо)",
                }
            ),
        }
