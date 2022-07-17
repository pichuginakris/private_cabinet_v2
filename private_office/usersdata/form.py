from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

User = get_user_model()


class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = User
        fields = ("username", "email", "phone_number")


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

    error_messages = {
        'invalid_login': _(
            "Пожалуйста, введите корректный номер телефона и пароль."
        ),
        'inactive': _("Аккаунт не активен. Пожалуйста, авторизуйтесь"),
    }
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={'minlength': 10, 'maxlength': 15, 'required': True,
                                        'type': 'tel', 'autocomplete': 'on'}))
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'on'}),
        strip=False,
        help_text=_("Enter the password."),
    )

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
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
            qs = User.objects.filter(phone_number=phone_number)
            if not qs.exists():
                raise forms.ValidationError(self.error_messages['invalid_login'],
                                            code='invalid_login' )
            else:
                raise forms.ValidationError(self.error_messages['invalid_login'],
                                            code='invalid_login')
        else:
            return data

    def login(self):
        data = self.cleaned_data
        phone_number = data.get('phone_number')
        password = data.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        return user

    def get_user(self):
        return self.user_cache

