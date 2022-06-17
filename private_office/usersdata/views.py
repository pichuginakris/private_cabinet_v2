from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect

from usersdata.form import UserCreation


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
            user = authenticate(phone_number=phone_number, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }

        return render(request, self.template_name, context)


def index(request):
    return render(request, 'usersdata/registration.html')
