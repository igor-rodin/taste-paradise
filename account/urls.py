from django.urls import path

from .views import (
    register,
    UserLogin,
    UserLogout,
    ProfileView,
    ChangeUserPassword,
    ChangeUserPasswordDone,
    profile_edit,
)

app_name = "account"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),
    path("password-change/", ChangeUserPassword.as_view(), name="change_password"),
    path(
        "password-change/done/",
        ChangeUserPasswordDone.as_view(),
        name="password_change_done",
    ),
    path("me/", ProfileView.as_view(), name="profile"),
    path("me/edit/", profile_edit, name="profile_edit"),
]
