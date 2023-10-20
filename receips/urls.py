from django.urls import path

from .views import add_receipe, index, DetailReceipe

app_name = "receips"

urlpatterns = [
    path("", index, name="index"),
    path("receipes/add", add_receipe, name="add_receipe"),
    path("receipes/<slug:rec_slug>", DetailReceipe.as_view(), name="receipe_detail"),
]
