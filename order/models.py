from django.db import models
from django.urls import reverse

from modelcluster.fields import ParentalKey

from account.models import CustomUser
from product.models import Product


class Order(models.Model):
    delivery = 'Пункт выдачи'
    self_delivery = 'Самовывоз'
    courier = 'Курьером'
    ship = [
        (delivery, 'Пункт выдачи'),
        (self_delivery, 'Самовывоз'),
        (courier, 'Курьером')
    ]
    awaiting_confirmation = 'Ожидает подтверждения'
    payment_error = 'Ошибка оплаты'
    canceled = 'Отменен'
    returned = 'Возвращен'
    partially_returned = 'Частично возвращен'
    in_processing = 'В обработке'
    not_paid = 'Не оплачен'
    paid = 'Оплачен'
    payment = [
        (awaiting_confirmation, 'Ожидает подтверждения'),
        (payment_error, 'Ошибка оплаты'),
        (canceled, 'Отменен'),
        (returned, 'Возвращен'),
        (partially_returned, 'Частично возвращен'),
        (in_processing, 'В обработке'),
        (not_paid, 'Не оплачен'),
        (paid, 'Оплачен')
    ]

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='email')
    city = models.CharField(max_length=50, verbose_name='Город/Поселок/Село/деревня')
    zip_code = models.CharField(max_length=6, verbose_name='Почтовый иднекс')
    ship_type = models.CharField(choices=ship, default=self_delivery, verbose_name='Тип доставки', max_length=50)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления заказа')
    payment_status = models.CharField(choices=payment, default=not_paid, max_length=50, verbose_name='Статус платежа')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Покупатель', related_name='order')
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    payment_id = models.CharField(max_length=50, verbose_name='Номер платежа', null=True, blank=True)
    confirmation_url = models.URLField(max_length=256, verbose_name='Ссылка на оплату платежа',
                                       blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.id}'

    def total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def total_discount_cost(self):
        return sum(item.get_discount_cost() for item in self.items.all())

    def get_absolute_url(self):
        return reverse('account:order_detail', kwargs={'id': self.id})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = ParentalKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Позиция')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    qty = models.PositiveIntegerField(default=1, verbose_name='Ко-во товара')
    size = models.CharField(max_length=10, verbose_name='Размер', blank=True, null=True)
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                         verbose_name='Цена товара со скидкой')

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return f'Позиция - {self.id}'

    def get_cost(self):
        return self.price * self.qty

    def get_discount_cost(self):
        return self.price_discount * self.qty
