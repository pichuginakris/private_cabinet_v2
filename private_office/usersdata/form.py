from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreation(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("phone_number", "password1", "password2")
        exclude = ['password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Ваш пароль должен содержать как минимум 8 символов.' \
                                             ' Пароль не может состоять только из цифр.'
        self.fields['password2'].help_text = 'Повторите пароль для подтверждения.'
        self.fields['phone_number'].error_messages['unique'] = 'Пользователь с таким номером телефона уже существует.'


class UserAuthorisation(AuthenticationForm):
    phone_number = forms.NumberInput()


    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['password'].help_text = 'Неверный пароль.'
    #    self.fields['phone_number'].error_messages['unique'] = 'Неверный номер телефона.'
