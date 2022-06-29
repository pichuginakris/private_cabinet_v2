from django.contrib.auth import get_user_model, authenticate
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


class UserAuthorisation(forms.Form):
    class Meta:
        model = User
        fields = ('phone_number', 'password')
    phone_number = forms.CharField(
                                     widget=forms.NumberInput(attrs={'minlength': 10, 'maxlength': 15, 'required': True, 'type': 'number'}))
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'on'}),
        strip=False,
        help_text=_("Enter the password."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.fields:
            field = self.fields.get(f)
            field.label = False

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        phone_number = data.get('phone_number')
        password = data.get('password')
        user = authenticate(phone_number=phone_number, password=password)

        if not user:
            qs = User.objects.filter(email=phone_number)
            if not qs.exists():
                raise forms.ValidationError('Email or Phone number not found.')
            else:
                raise forms.ValidationError('Sorry, password is wrong.')
        else:
            return data

    def login(self):
        data = self.cleaned_data
        phone_number = data.get('phone_number')
        password = data.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        return user

