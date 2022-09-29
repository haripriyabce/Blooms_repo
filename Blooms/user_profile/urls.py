from django.urls import path
from .import views
urlpatterns = [
    path('myaddresses',views.myaddresses,name='myaddresses'), 
    path('make_default/<int:id>/',views.make_default,name='make_default'),
    path('up_address/<int:id>/',views.up_address,name='up_address'),
    path('add_address',views.add_address,name='add_address'),
    path('remove_add/<int:id>/',views.remove_add,name='remove_add'),
    
    
    path('myprofile',views.myprofile,name='myprofile'),
    path('profile_up',views.profile_edit,name='profile_up'),
    path('change_password',views.change_password,name='change_password'),
    
    path('myorders',views.myorders,name='myorders'),    
    path('myorder_details/<int:id>',views.myorders_de,name='myorder_details'),
    path('mycancel/<int:id>', views.mycancel_order,name='mycancel'),    
    path('export_invoice_pdf/<int:id>',views.export_invoice_pdf,name='export_invoice_pdf'),
    path('invoice/<int:id>',views.invoice,name='invoice'),
    path('track_order/<int:id>',views.track_order,name='track_order'),
    path('review/<int:id>',views.review,name='review'),
    
    
    
    path('coupons',views.coupon_list,name='coupons'),   
   
    
    path('wishlist',views.wishlist,name='wishlist'),
    path('add_wishlist/<int:id>',views.add_wishlist,name='add_wishlist'),
    path('wishlist_remove/<int:id>',views.wishlist_remove,name='wishlist_remove'),


]