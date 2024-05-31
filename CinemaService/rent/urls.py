from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('remove_cart_item/<cart_item_uid>', remove_cart_item, name='remove_cart'),
    path('add_cart/<movie_uid>', add_cart, name='add_cart'),
    path('update_cart_item_quantity/<cart_item_uid>/', update_cart_item_quantity, name='update_cart_item_quantity'),
    path('movie/<movie_uid>', movie, name='movie_page'),
    path('clear_cart/', clear_cart, name='clear_cart')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
