from django.urls import path, include

from .views import Register, Login

from . import views

urlpatterns = [

    path('ex/', views.index),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),


]