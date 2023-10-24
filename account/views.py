from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from .forms import RegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView


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


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            if new_user:
                username = form.cleaned_data.get("username")
                pwd = form.cleaned_data.get("password1")
                new_user = authenticate(request, username=username, password=pwd)
                login(request, user=new_user)
                return redirect("receips:all_receipes")
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = RegisterForm()
    return render(
        request, template_name="account/register.html", context={"form": form}
    )
