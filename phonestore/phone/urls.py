from .models import Category, Product, User
from . import views
from django.urls import path
# from django.contrib import admin
from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path('', views.main, name = 'name'),
    path('categorys/', views.category_list, name='categorys'),
    path('categorys/products/<int:id>', views.product_detail, name = 'products'),
    path('login/', views.sign_in, name='login'),
    path('register/', views.sign_up, name='register'),
    path('search/', views.search_feature, name='search-box'),
    path('page_user/', views.page_user, name='user'),
    path('logout/', views.logout_view, name='logout'),
    path('order/', views.order_page, name='order'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
