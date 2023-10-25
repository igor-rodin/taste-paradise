from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from taggit.models import Tag

from .forms import ReceipeForm
from .models import Receipe, Category
from account.models import Profile


def index(request: HttpRequest) -> HttpResponse:
    show_receipes = 5
    receips = (
        Receipe.objects.select_related("author")
        .prefetch_related("tags", "user_likes")
        .all()[: show_receipes + 1]
    )

    profile = None
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user__pk=request.user.pk)
    categories = Category.objects.all()
    context = {"categories": categories, "receips": receips, "user_profile": profile}

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


class UpdateReceipeView(UserPassesTestMixin, UpdateView):
    model = Receipe
    template_name = "receips/add_receipe.html"
    form_class = ReceipeForm
    context_object_name = "receipe"
    success_url = reverse_lazy("receips:all_receipes")
    slug_url_kwarg = "rec_slug"

    def test_func(self) -> bool | None:
        rec_obj = (
            Receipe.objects.select_related("author")
            .filter(slug=self.kwargs["rec_slug"])
            .first()
        )
        return self.request.user == rec_obj.author


class ListReceipe(ListView):
    model = Receipe
    template_name = "receips/receipes.html"
    context_object_name = "receips"
    paginate_by = 4

    def get_queryset(self):
        slug = self.kwargs.get("cat_slug")
        searched_value = None
        if self.request.GET:
            searched_value = self.request.GET["search"]
        if slug and searched_value:
            return Receipe.objects.select_related("author").filter(
                category__slug=slug, title__icontains=searched_value
            )
        if slug:
            return Receipe.objects.select_related("author").filter(category__slug=slug)
        if searched_value:
            return Receipe.objects.select_related("author").filter(
                title__icontains=searched_value
            )
        return Receipe.objects.select_related("author").all()


@login_required(login_url="account:login")
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
