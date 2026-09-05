from django.shortcuts import render, get_object_or_404, redirect
from users.models import User
from books.models import Book

from orders.models import OrderItem
from orders.cart.cart import Cart
from orders.forms import OrderCreateForm
# Create your views here.

def cart_add(request, pk):
    cart = Cart(request)
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add_item(book, quantity)
    return redirect('payment:cart_detail')

def cart_detail(request):
    cart = Cart(request)

    context = {"cart": cart, "total_price": cart.get_total()}
    return render(request, 'cart/cart_detail.html', context)

def cart_remove(request, pk):
    cart = Cart(request)
    book = get_object_or_404(Book, pk=pk)
    cart.remove(book)
    return redirect('payment:cart_detail')

def order_create(request):
    cart = Cart(request)
    if not cart.cart:
        return redirect('cart_detail')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total()
            if request.user.is_authenticated:
                try:
                    order.email = request.user.email
                except:
                    email, _ = User.objects.get_or_create(email=request.user.email)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, book=item['book'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/success.html', {'order': order})
    else:
        defaults = {}
        if request.user.is_authenticated:
            defaults = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=defaults)
    context = {'form': form, 'cart': cart, 'total_price': cart.get_total()}

    return render(request, 'orders/order_create.html', context)
