from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import datetime


class User(AbstractUser):
    username = models.CharField('Имя пользователя', default='Введите имя', max_length=1000)
    email = models.CharField('Почта', max_length=1000)
    date = models.DateField('Дата первого занятия', default=datetime.date.today)
    phone_number = PhoneNumberField('Номер телефона', unique=True, null=False, blank=False)
    password = models.CharField('Пароль', max_length=100)
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return str(self.phone_number)
