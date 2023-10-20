from django import forms

from .models import Receipe, Category


class ReceipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Выбор категории",
        empty_label="Категория...",
        widget=forms.Select(attrs={"class": "form-control"}),
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
            "image",
            "tags",
        )
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "cooking_steps": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "ingredient": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "tags": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "(Введите теги через запятую)",
                }
            ),
        }
