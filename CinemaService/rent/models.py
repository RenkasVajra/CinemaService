from django.db import models
from users.models import SiteUser
import uuid


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, verbose_name='UID', editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now_add=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True


class MovieCategory(BaseModel):
    category_name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        db_table = 'Categories'


class Movie(BaseModel):
    category = models.ForeignKey(
        MovieCategory,
        on_delete=models.CASCADE,
        related_name="pizzas",
        verbose_name='Категория'
    )
    movie_name = models.CharField(max_length=100, verbose_name='Название')
    price = models.IntegerField(default=100, verbose_name='Цена')
    images = models.ImageField(max_length=500, upload_to='staticfiles', verbose_name='Изображение')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    date_created = models.DateField(null=True, verbose_name='Дата Создания')

    class Meta:
        db_table = 'Movies'


class Cart(BaseModel):
    user = models.ForeignKey(
        SiteUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Имя пользователя',
        related_name='carts'
    )
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')

    class Meta:
        db_table = 'Carts'


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Название')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    class Meta:
        db_table = 'CartItems'
