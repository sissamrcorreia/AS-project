"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from .views import home, product_list, exit, register, create_product, edit_product, delete_product, profile, buy_product, statistics
from allauth.mfa.base.views import IndexView
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('create-product/', create_product, name='create_product'),
    path('edit-product/<int:pk>/', edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
    path('buy/<int:product_id>/', buy_product, name='buy_product'),
    path('profile/<str:username>/', profile, name='profile'),
    path('statistics/', statistics, name='statistics')
]