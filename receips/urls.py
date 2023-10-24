from django.urls import path

from .views import add_receipe, index, DetailReceipe, ListReceipe, get_receipes_by_tag

app_name = "receips"

urlpatterns = [
    path("", index, name="index"),
    path("receipes/cat/", ListReceipe.as_view(), name="all_receipes"),
    path(
        "receipes/detail/<slug:rec_slug>/",
        DetailReceipe.as_view(),
        name="receipe_detail",
    ),
    path("receipes/cat/<slug:cat_slug>/", ListReceipe.as_view(), name="all_receipes"),
    path(
        "receipes/tags/<slug:tag_slug>/", get_receipes_by_tag, name="receipes_by_tags"
    ),
    path("receipes/add/", add_receipe, name="add_receipe"),
]
