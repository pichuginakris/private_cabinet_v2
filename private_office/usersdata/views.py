from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from .form import UserCreation, UserAuthorisation, UpdateProfileForm, PasswordChange
from .db_connection import choose_category
from django.contrib.auth.decorators import login_required
from .models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreation()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreation(request.POST)

        if form.is_valid():
            form.save()
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
            print(form.error_messages)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class Login(View):
    template_name = 'registration/login.html'

    def get(self, request):
        context = {
            'form': UserAuthorisation()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserAuthorisation(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
            print(form.error_messages)

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def password_change(request):
    if request.method == 'POST':
        change_form = PasswordChangeForm(request.user, request.POST)
        if change_form.is_valid():
            user = change_form.save()
            update_session_auth_hash(request, user)
            data = {"change_form": change_form}
    else:
        change_form = PasswordChangeForm(request.user)
        data = {"change_form": change_form}
    return render(request, 'registration/password_change.html', context=data)


def index(request):
    return render(request, 'usersdata/registration.html')


@login_required
def profile(request):
    try:
        # category_names = choose_category()
        category_names = ['Выберите категорию', '']
    except:
        category_names = ['Выберите категорию', '']
    data = {"category_names": category_names}
    return render(request, 'registration/profile.html', context=data)


@login_required
def profile_change(request):
    try:
        # category_names = choose_category()
        category_names = ['Выберите категорию', '']
    except:
        category_names = ['Выберите категорию', '']

    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(to='/users/profile')
    else:
        profile_form = UpdateProfileForm(instance=request.user)
    data = {"category_names": category_names, 'profile_form': profile_form}
    return render(request, 'registration/profile_change.html', context=data)


