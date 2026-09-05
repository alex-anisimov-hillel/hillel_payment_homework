from django.contrib.auth.decorators import permission_required, login_required
from django.urls import path

from books import views as books_views
urlpatterns = [
    path("", books_views.BooksListView.as_view(), name="book_list"),
    path("<pk>", books_views.BookDetailView.as_view(), name="book_detail"),
    path("admin/create/<pk>", books_views.BookCreateView.as_view(), name="book_create"),
    path("admin/edit/<pk>", books_views.BookEditView.as_view(), name="book_update"),
    path("admin/delete/<pk>", books_views.BookDeleteView.as_view(), name="book_delete"),
]