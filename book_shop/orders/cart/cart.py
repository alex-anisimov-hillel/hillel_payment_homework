from django.conf import settings
from books.models import Book

class Cart:
    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_item(self, book: Book, quantity=1, override_quantity=False):
        book_id = str(book.id)
        if book not in self.cart:
            self.cart[book_id] = {'quantity': 0, 'price': str(book.price)}

        if quantity <= 0:
            quantity = 1
        if override_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, book: Book):
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]


    def __iter__(self):
        books_ids = self.cart.keys()
        books = Book.objects.filter(id__in=books_ids)
        for book in books:
            self.cart[str(book.id)]['book'] = book
        for item in self.cart.values():
            item['total_price'] = float(item['price']) * int(item['quantity'])
            yield item

    def get_total(self):
        return sum(float(item['price'])*int(item['quantity']) for item in self.cart.values())