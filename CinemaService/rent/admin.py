from django.contrib import admin
from .models import *


class MovieCategoryAdmin(admin.ModelAdmin):
    model = MovieCategory
    list_display = ("category_name",)
    search_fields = ("category_name",)


class MovieAdmin(admin.ModelAdmin):
    model = Movie
    list_display = ("category", "movie_name", "price", "images", "description", "date_created")
    search_fields = ("category", "movie_name", "price", "images", "description", "date_created")


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ("user", "is_paid")
    search_fields = ("user", "is_paid")


class CartItemsAdmin(admin.ModelAdmin):
    model = CartItems
    list_display = ("cart", "showtime", "seat")
    search_fields = ("cart", "showtime", "seat")


class ShowtimeAdmin(admin.ModelAdmin):
    model = Showtime
    list_display = ("movie", "date", "time")
    search_fields = ("cart", "showtime", "quantity")


class SeatAdmin(admin.ModelAdmin):
    model = Seat
    list_display = ("showtime", "row", "number", "is_available", "is_booked")
    search_fields = ("showtime", "row", "number", "is_available", "is_booked")


admin.site.register(MovieCategory, MovieCategoryAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItems, CartItemsAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Showtime, ShowtimeAdmin)
