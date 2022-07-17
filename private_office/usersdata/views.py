from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from .form import UserCreation, UserAuthorisation, UpdateProfileForm
from .db_connection import choose_category
from django.contrib.auth.decorators import login_required
from .models import User


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
