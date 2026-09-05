import logging
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from books.models import Book

logger = logging.getLogger(__name__)

class LoggingMixin:
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"User went to: {request.path}. User email: {request.user.email}")
        response = super().dispatch(request, *args, **kwargs)
        logger.info("STATUS CODE " + str(response.status_code))

        return response


class BooksListView(LoggingMixin, LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    template_name = 'book_create.html'
    context_object_name = 'book'
    fields = '__all__'
    permission_required = 'books.add_book'

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'book_delete.html'
    context_object_name = 'book'
    permission_required = 'books.delete_book'

class BookEditView(PermissionRequiredMixin, UpdateView):
    model = Book
    template_name = 'book_update.html'
    context_object_name = 'book'
    fields = '__all__'
    permission_required = 'books.change_book'