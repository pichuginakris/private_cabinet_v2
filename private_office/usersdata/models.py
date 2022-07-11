from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import datetime


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("User must have a phone_number")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            phone_number=phone_number
        )
        user.set_password(password)  # change password to hash
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number,  password=None, **extra_fields):
        if not phone_number:
            raise ValueError("User must have a phone number")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            phone_number=phone_number
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField('Имя пользователя', default='Введите имя', max_length=1000)
    email = models.CharField('Почта', max_length=1000)
    date = models.DateField('Дата первого занятия', default=datetime.date.today)
    phone_number = PhoneNumberField('Номер телефона', unique=True, null=False, blank=False, region='RU')
    password = models.CharField('Пароль', max_length=100)
    USERNAME_FIELD = 'phone_number'
    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)


class Category(models.Model):
    phone_number = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)