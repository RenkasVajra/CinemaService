import hashlib
import hmac
import requests

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import *


SHOP_ID = '86A8A0BDD9A7227413AFD532E5347F81E607DA029BA0092578CFB6563468F551'
SECRET_KEY = 'YOUR_SECRET_KEY'


def home(request):
    context = {}
    movies = Movie.objects.all()
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
        quantity = cart.cart_items.aggregate(total=models.Sum('quantity'))['total'] or 0
        context['quantity'] = quantity
    else:
        pass
    context['movies'] = movies
    return render(request, 'home.html', context)


def movie(request, movie_uid):
    movie_obj = get_object_or_404(Movie, uid=movie_uid)
    context = {'movie': movie_obj}
    return render(request, 'movie.html', context)


@login_required(login_url='/login/')
def add_cart(request, movie_uid):
    user = request.user
    movie_obj = Movie.objects.get(uid=movie_uid)
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItems.objects.get_or_create(cart=cart, movie=movie_obj)
    cart_item.quantity = quantity
    cart_item.save()

    return redirect('/')


@login_required(login_url='/login/')
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    quantity = cart.cart_items.aggregate(total=models.Sum('quantity'))['total'] or 0
    context = {'carts': cart, 'quantity': quantity}
    return render(request, 'cart.html', context)


@login_required(login_url='/login/')
def clear_cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    cart.cart_items.all().delete()
    return redirect('/cart/')


@login_required(login_url='/login/')
def remove_cart_item(request, cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()
        return redirect('/cart/')
    except Exception as e:
        print(e)


@require_POST
@login_required(login_url='/login/')
def update_cart_item_quantity(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)
        new_quantity = int(request.POST.get('quantity'))

        if new_quantity < 1 or new_quantity > 20:
            return JsonResponse({'success': False, 'error': 'Invalid quantity'})

        cart_item.quantity = new_quantity
        cart_item.save()

        # Обновляем количество товаров в корзине
        cart = Cart.objects.get(is_paid=False, user=request.user)
        quantity = cart.cart_items.aggregate(total=models.Sum('quantity'))['total'] or 0

        return JsonResponse({'success': True, 'quantity': quantity})
    except CartItems.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart item does not exist'}, status=404)


@login_required(login_url='/login/')
def checkout(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    total_price = cart.cart_items.aggregate(total=models.Sum('total_price'))['total'] or 0
    success_url = request.build_absolute_uri("/payment/success/")
    fail_url = request.build_absolute_uri("/payment/fail/")
    context = {'total_price': total_price, 'success_url': success_url, 'fail_url': fail_url}
    return render(request, 'checkout.html', context)

@csrf_exempt
@login_required(login_url='/login/')
def payment(request):
    if request.method == 'POST':
        cart = Cart.objects.get(is_paid=False, user=request.user)
        total_price = float(request.POST.get('amount'))

        # Формируем данные для запроса в Yoomoney
        payment_data = {
            "receiver": SHOP_ID,  # ID вашего магазина
            "quickpay-form": "shop",
            "targets": request.POST.get('label'),  # Описание платежа
            "sum": total_price,
            "successURL": request.POST.get('success_url'),
            "failURL": request.POST.get('fail_url'),
            "paymentType": "PC",  # Оплата картой
            "label": "Оплата билетов в кино",
        }

        # Подписываем данные  HMAC-SHA256  с помощью секретного ключа
        sign = hmac.new(SECRET_KEY.encode(), str(payment_data).encode(), hashlib.sha256).hexdigest()
        payment_data["sign"] = sign

        try:
            # Отправляем запрос в Yoomoney
            response = requests.post(
                "https://yoomoney.ru/quickpay/confirm.xml",
                data=payment_data,
            )

            # Обрабатываем ответ Yoomoney (посмотрите документацию)
            if response.status_code == 200:
                # Перенаправляем пользователя на страницу оплаты Yoomoney
                return redirect(response.text)
            else:
                return JsonResponse({'error': 'Ошибка при обработке платежа'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return redirect('cart')

@login_required(login_url='/login/')
def payment_success(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    cart.is_paid = True
    cart.save()
    cart.cart_items.all().delete()
    return render(request, 'success.html')

@login_required(login_url='/login/')
def payment_fail(request):
    return render(request, 'cancel.html')