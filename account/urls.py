from django.urls import path

from .views import register, UserLogin, UserLogout

app_name = "account"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),
]
