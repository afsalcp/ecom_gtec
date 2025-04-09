from django.urls import path
from . import views

urlpatterns=[
    path('',views.Login.as_view(),name='login'),
    path('signup/',views.Signup.as_view(),name='signup'),
    path('product/',views.product_data,name='product'),
    path('cart/add',views.add_to_cart,name='add_to_cart'),
    path('cart/remove',views.remove_from_cart,name='remove_from_cart'),
    path('cart',views.cart,name='cart')
]