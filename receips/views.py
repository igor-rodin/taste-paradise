from typing import Any
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView


from .forms import ReceipeForm
from .models import Receipe


def index(request: HttpRequest) -> HttpResponse:
    show_receipes = 3
    receips = Receipe.objects.select_related("author", "category").all()[
        1 : show_receipes + 1
    ]
    return render(
        request, template_name="receips/index.html", context={"receips": receips}
    )


class DetailReceipe(DetailView):
    model = Receipe
    template_name = "receips/receipe_detail.html"
    context_object_name = "receipe"

    def get_object(self, queryset=None):
        return (
            Receipe.objects.filter(slug=self.kwargs["rec_slug"])
            .select_related("author", "category")
            .first()
        )


@login_required
def add_receipe(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ReceipeForm(request.POST)
        if form.is_valid():
            receipe: Receipe = form.save(commit=False)
            receipe.author = request.user
            receipe.save()
            form.save_m2m()
            return redirect("receips:receips")
    else:
        form = ReceipeForm(request.POST)
    return render(
        request, template_name="receips/add_receipe.html", context={"form": form}
    )
