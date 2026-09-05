"""
URL configuration for book_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from book_shop import settings
from payment.views import checkout_view

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path("accounts/login", include('django.contrib.auth.urls')),
    path("accounts/register", include('users.urls')),
    path("books/", include('books.urls')),
    path("payment/", include('payment.urls')),
    path(r'^__debug__/', include(debug_toolbar.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

'''path("books/<pk>", include('books.urls')),
path("books/admin/create/<pk>", include('books.urls')),
path("books/admin/edit/<pk>", include('books.urls')),
path("books/admin/delete/<pk>", include('books.urls')),'''