from django.urls import path
from .import views
urlpatterns = [
    path('add_cart', views.add_cart, name='add_cart'), 
    path('cart', views.cart,name='cart'),    
    path('apply_coupon', views.apply_coupon,name='apply_coupon'), 
    path('delete_cart_product/<int:id>/',views.delete_cart_product,name='delete_cart_product'),
    path('update_cart/<int:id>/',views.update_cart,name='update_cart'),
    path('checkt_add', views.checkt_add,name='checkt_add'),
    path('paypal_success', views.paypal_success,name='paypal_success'),
    path('checkt_pay', views.checkt_pay,name='checkt_pay'),
    path('pay_success', views.pay_success,name='pay_success'),
    path('cash_on_delivery', views.cash_on_delivery,name='cash_on_delivery'),    
    path('show_addresses/',views.show_addresses,name='show_addresses'),
    
]