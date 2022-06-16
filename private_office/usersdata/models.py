from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime


class User(models.Model):
    username = models.TextField('Имя пользователя')
    email = models.CharField('Почта', max_length=1000)
    date = models.DateField('Дата первого занятия', default=datetime.date.today)
    phone_number = PhoneNumberField('Номер телефона', unique=True, null=False, blank=False)
    password = models.CharField('Пароль', max_length=100)

    def __set__(self):
        return self.username
