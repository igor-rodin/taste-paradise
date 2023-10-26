from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

from .forms import (
    RegisterForm,
    UserLoginForm,
    UserChangePasswordForm,
    UserEditForm,
    ProfileEditForm,
)
from .models import Profile
from receips.models import Receipe


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "account/register.html"
    success_url = reverse_lazy("receips:all_receipes")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        pwd = form.cleaned_data.get("pwd")
        new_user = authenticate(self.request, username=username, password=pwd)
        login(self.request, user=new_user)
        return response


class UserLogin(LoginView):
    template_name = "account/login.html"
    form_class = UserLoginForm
    redirect_authenticated_user = True


class UserLogout(LogoutView):
    next_page = reverse_lazy("receips:index")


class ChangeUserPassword(PasswordChangeView):
    template_name = "account/change_password.html"
    form_class = UserChangePasswordForm
    success_url = reverse_lazy("account:password_change_done")


class ChangeUserPasswordDone(PasswordChangeDoneView):
    template_name = "account/change_password_done.html"


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            if new_user:
                username = form.cleaned_data.get("username")
                pwd = form.cleaned_data.get("password1")
                new_user = authenticate(request, username=username, password=pwd)
                Profile.objects.create(user=new_user)
                login(request, user=new_user)
                return redirect("receips:all_receipes")
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = RegisterForm()
    return render(
        request, template_name="account/register.html", context={"form": form}
    )


class ProfileView(DetailView):
    model = Profile
    template_name = "account/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        profile = (
            Profile.objects.select_related("user")
            .filter(user__pk=self.request.user.pk)
            .first()
        )
        return profile

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        receipes = Receipe.objects.filter(author__pk=self.request.user.pk)
        context.update({"receipes": receipes})
        return context


@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse_lazy("account:profile"))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        template_name="account/profile_edit.html",
        context={"user_form": user_form, "profile_form": profile_form},
    )
