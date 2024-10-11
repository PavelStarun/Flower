from django.db import models
from django.contrib.auth.models import User

from django.conf import settings



class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    status = models.CharField(max_length=20, choices=[
        ('Processing', 'Обрабатывается'),
        ('Shipped', 'Отправлен'),
        ('Delivered', 'Доставлен')
    ], default='Processing', verbose_name="Статус заказа")

    def __str__(self):
        return f'Заказ {self.id} от {self.user.username}'
