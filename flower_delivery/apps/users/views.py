from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileEditForm


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
        else:
            if form.non_field_errors():
                for error in form.non_field_errors():
                    if error == "Please enter a correct username and password.":
                        messages.error(request, "Неверный пароль или имя пользователя.")
                    else:
                        messages.error(request, error)
            else:
                messages.error(request, "Ошибка авторизации. Проверьте данные.")
        return render(request, "users/login.html", {"form": form})


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
        else:
            print(form.errors)
        return render(request, "users/register.html", {"form": form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "users/profile.html")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("login")


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserProfileEditForm(instance=request.user)
        return render(request, "users/profile_edit.html", {"form": form})

    def post(self, request):
        form = UserProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "users/profile_edit.html", {"form": form})
