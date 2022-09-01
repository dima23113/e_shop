from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    email_mailing = models.BooleanField(default=True, verbose_name='Рассылка акций и предложений', blank=True,
                                        null=True)
    phone = models.CharField(max_length=256, verbose_name='Телефон', blank=True, null=True)
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserAddress(models.Model):
    ru = 'Россия'
    ukr = 'Украина'
    blr = 'Беларусь'
    countries = [
        (ru, 'Россиия'),
        (ukr, 'Украина'),
        (blr, 'Беларусь')
    ]
    address_name = models.CharField(max_length=256, verbose_name='Название адреса')
    country = models.CharField(max_length=256, verbose_name='Страна', choices=countries, default=ru)
    city = models.CharField(max_length=256, verbose_name='Город')
    street = models.CharField(max_length=256, verbose_name='Улица')
    street_number = models.CharField(max_length=256, verbose_name='Номер улицы')
    zip_code = models.CharField(max_length=256, verbose_name='Почтовый индекс')
    comment = models.CharField(max_length=256, verbose_name='Комментарий к адресу')
    phone = models.CharField(max_length=256, verbose_name='Номер телефона')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_addresses')

    def __str__(self):
        return f'{self.user} - {self.address_name}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
