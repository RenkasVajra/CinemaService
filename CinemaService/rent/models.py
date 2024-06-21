from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.formats import date_format, time_format

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

    def __str__(self):
        return self.category_name

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
    duration = models.TextField(max_length=30, verbose_name='Длительность')
    country = models.TextField(max_length=100, verbose_name='Страна')
    director = models.TextField(max_length=300, verbose_name='Режиссер')
    script = models.TextField(max_length=300, verbose_name='Сценарий')
    producer = models.TextField(max_length=300, verbose_name='Продюсер')
    composer = models.TextField(max_length=300, verbose_name='Композитор')

    def __str__(self):
        return self.movie_name

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

    def get_total_price(self):
        return sum(item.showtime.movie.price for item in self.cart_items.all())


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.movie.movie_name} - {date_format(self.date, 'Y-m-d')} {time_format(self.time, 'H:i')}"

    class Meta:
        db_table = 'rent_showtime'


class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    row = models.CharField(max_length=2)  # Например, "A", "B", "C"
    number = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.showtime} - Ряд {self.row}, Место {self.number}"

    class Meta:
        db_table = 'rent_seat'


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Название')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, verbose_name='Сеанс')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name='Место')

    class Meta:
        db_table = 'CartItems'

    def __str__(self):
        return str(self.cart)


@receiver(post_save, sender=Showtime)
def create_seats_for_showtime(sender, instance, created, **kwargs):
    if created:
        for row in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            for number in range(1, 9):
                Seat.objects.create(showtime=instance, row=row, number=number)
