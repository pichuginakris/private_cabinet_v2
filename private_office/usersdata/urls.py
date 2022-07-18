from django.urls import path, include
from django.contrib.auth import views as django_views
from .views import Register, Login
from . import views

urlpatterns = [
    path('ex/', views.index),
    path('profile/', views.profile),
    path('change/', views.profile_change),
    path('logout/', django_views.LogoutView.as_view(), name='logout'),

    #path('password_change/', django_views.PasswordChangeView.as_view(), name='password_change'),
    #path('password-reset/', views.ChangePassword.as_view(), name='password-reset'),
    path('password_change/', views.password_change),
    path('password_change/done/', django_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', django_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', django_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', django_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', django_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]