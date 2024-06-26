import hashlib
import hmac
import requests

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *


SHOP_ID = '86A8A0BDD9A7227413AFD532E5347F81E607DA029BA0092578CFB6563468F551'
SECRET_KEY = 'YOUR_SECRET_KEY'


def home(request):
    movies = Movie.objects.all()
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
        quantity = cart.cart_items.count()

    else:
        quantity = 0
    return render(request, 'home.html', context={'quantity': quantity, 'movies': movies})


@login_required
def movie(request, movie_uid):
    movie = Movie.objects.get(uid=movie_uid)
    showtimes = Showtime.objects.filter(movie=movie)
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_items = cart.cart_items.all()
    quantity = cart.cart_items.count()

    unique_dates = []
    for showtime in showtimes:
        if showtime.date not in unique_dates:
            unique_dates.append(showtime.date)

    context = {
        'movie': movie,
        'showtimes': showtimes,
        'unique_dates': unique_dates,
        'quantity': quantity,
    }
    return render(request, 'movie.html', context)


@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_items = cart.cart_items.all().order_by('created_at')
    quantity = cart.cart_items.count()
    total_price = cart.get_total_price()
    paginator = Paginator(cart_items, 10)
    page = request.GET.get('page')
    try:
        cart_items = paginator.get_page(page)
    except PageNotAnInteger:
        cart_items = paginator.page(1)
    except EmptyPage:
        cart_items = paginator.page(paginator.num_pages)

    context = {
        'carts': cart,
        'cart_items': cart_items,
        'quantity': quantity,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='/login/')
def clear_cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)

    seats_in_cart = cart.cart_items.all().values_list('seat', flat=True)

    for seat_id in seats_in_cart:
        seat = Seat.objects.get(pk=seat_id)
        seat.is_available = True
        seat.is_booked = False
        seat.booked_by = None
        seat.save()

    cart.cart_items.all().delete()
    return redirect('/cart/')


@login_required(login_url='/login/')
def remove_cart_item(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)

        cart_item.seat.is_available = True
        cart_item.seat.is_booked = False
        cart_item.seat.booked_by = None
        cart_item.seat.save()

        cart_item.delete()
        return redirect('/cart/')
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Ошибка при удалении товара.'})


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

        payment_data = {
            "receiver": SHOP_ID,
            "quickpay-form": "shop",
            "targets": request.POST.get('label'),
            "sum": total_price,
            "successURL": request.POST.get('success_url'),
            "failURL": request.POST.get('fail_url'),
            "paymentType": "PC",
            "label": "Оплата билетов в кино",
        }

        sign = hmac.new(SECRET_KEY.encode(), str(payment_data).encode(), hashlib.sha256).hexdigest()
        payment_data["sign"] = sign

        try:
            response = requests.post(
                "https://yoomoney.ru/quickpay/confirm.xml",
                data=payment_data,
            )

            if response.status_code == 200:
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

@login_required
def book_tickets(request, showtime_id):
    showtime = Showtime.objects.get(pk=showtime_id)
    movie = showtime.movie
    seats = Seat.objects.filter(showtime=showtime)


@login_required
def add_cart(request, movie_uid):
    movie_obj = Movie.objects.get(uid=movie_uid)
    if request.method == 'POST':
        showtime_id = request.POST.get('showtime_id')
        selected_seats_str = request.POST.get('selected_seats')
        print('selected_seats_str', selected_seats_str)
        if showtime_id and selected_seats_str:
            showtime = Showtime.objects.get(pk=showtime_id)
            selected_seats = [int(seat_id) for seat_id in selected_seats_str.split(',') if seat_id]

            if all(Seat.objects.get(pk=seat_id).is_available for seat_id in selected_seats):
                for seat_id in selected_seats:
                    seat = Seat.objects.get(pk=seat_id)
                    seat.booked_by = request.user
                    seat.is_available = False
                    seat.is_booked = True
                    seat.save()

                cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
                for seat_id in selected_seats:
                    seat = Seat.objects.get(pk=seat_id)
                    CartItems.objects.create(cart=cart, showtime=showtime, seat=seat)

                return redirect('select_seats', showtime_id=showtime_id)
            else:
                return JsonResponse({'success': False, 'error': 'Некоторые места недоступны.'})
        else:
            return JsonResponse({'success': False, 'error': 'Неверные данные.'})
    else:
        return JsonResponse({'success': False, 'error': 'Неверный запрос.'})

@login_required
def select_seats(request, showtime_id):
    showtime = Showtime.objects.get(pk=showtime_id)
    movie = showtime.movie
    seats = Seat.objects.filter(showtime=showtime)
    context = {
        'showtime': showtime,
        'movie': movie,
        'seats': seats,
    }

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
        quantity = cart.cart_items.count() or 0
        context['quantity'] = quantity
    else:
        context['quantity'] = 0

    return render(request, 'select_seats.html', context)


@login_required
def get_cart_items(request, showtime_id):
    showtime = Showtime.objects.get(pk=showtime_id)
    cart_items = CartItems.objects.filter(cart__user=request.user, showtime=showtime)
    cart_items_data = [{'seat': item.seat.id} for item in cart_items]
    return JsonResponse({'cart_items': cart_items_data})


@login_required
def showtime_time(request, showtime_date):
    showtimes = Showtime.objects.filter(date=showtime_date)
    movie = showtimes[0].movie
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    quantity = cart.cart_items.count()
    context = {
        'quantity': quantity,
        'showtimes': showtimes,
        'movie': movie,
    }

    return render(request, 'show_time.html', context)

