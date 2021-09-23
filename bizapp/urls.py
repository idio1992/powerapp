from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories', views.categories, name='categories'),
    path('all_products', views.all_products, name='all_products'),
    path('prod_category/<str:id>/', views.prod_category, name='prod_category'),
    path('detail/<str:id>/', views.prod_detail, name='detail'),
    path('loginform', views.loginform, name='loginform'),
    path('logoutform', views.logoutform, name='logoutform'),
    path('signupform', views.signupform, name='signupform'),
    path('profile', views.profile, name='profile'),
    path('update', views.update, name='update'),
    path('password', views.password, name='password'),
    path('shopcart', views.shopcart, name='shopcart'),
    path('cart', views.cart, name='cart'),
    path('increase', views.increase, name='increase'),
    path('remove', views.remove, name='remove'),
    path('checkout', views.checkout, name='checkout'),
    path('paidorder', views.paidorder, name='paidorder'),
    path('completed', views.completed, name='completed')
]
