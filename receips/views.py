from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView

from taggit.models import Tag

from .forms import ReceipeForm
from .models import Receipe, Category


def index(request: HttpRequest) -> HttpResponse:
    show_receipes = 5
    receips = (
        Receipe.objects.select_related("author")
        .prefetch_related("tags", "user_likes")
        .all()[: show_receipes + 1]
    )

    categories = Category.objects.all()
    context = {"categories": categories, "receips": receips}

    return render(request, template_name="receips/index.html", context=context)


def get_receipes_by_tag(request: HttpRequest, tag_slug):
    receips = Receipe.objects.all().select_related("author").filter(tags__slug=tag_slug)

    return render(
        request, template_name="receips/receipes.html", context={"receips": receips}
    )


class DetailReceipe(DetailView):
    model = Receipe
    template_name = "receips/receipe_detail.html"
    context_object_name = "receipe"

    def get_object(self, queryset=None):
        return (
            Receipe.objects.filter(slug=self.kwargs["rec_slug"])
            .select_related("author", "category")
            .prefetch_related("tags", "user_likes")
            .first()
        )


class ListReceipe(ListView):
    model = Receipe
    template_name = "receips/receipes.html"
    context_object_name = "receips"

    def get_queryset(self):
        slug = self.kwargs.get("cat_slug")
        if slug:
            return Receipe.objects.select_related("author").filter(category__slug=slug)
        return Receipe.objects.select_related("author").all()


@login_required
def add_receipe(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ReceipeForm(request.POST, request.FILES)
        if form.is_valid():
            receipe: Receipe = form.save(commit=False)
            receipe.author = request.user
            receipe.save()
            form.save_m2m()
            return redirect("receips:all_receipes")
    else:
        form = ReceipeForm(request.POST)
    return render(
        request, template_name="receips/add_receipe.html", context={"form": form}
    )
