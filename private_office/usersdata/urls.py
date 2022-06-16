from django.urls import path, include

from usersdata.views import Register

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('ex/', views.index),
    path('register/', Register.as_view(), name='register'),
]