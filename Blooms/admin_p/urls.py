from django.urls import path
from .import views
urlpatterns = [
    path('user',views.user,name='user'),   
    path('update_cat/<int:id>', views.update_cat,name='update_cat'),
    path('update_subcat/<int:id>', views.update_subcat,name='update_subcat'),
    path('product_edit/<int:id>', views.product_edit,name='product_edit'),
    #path('update/update_user2/<int:id>', views.update_user2),    
    path('deactivate/<int:id>', views.deactivate_cat),
    path('block_unblock/<int:id>', views.block_unblock,name='block_unblock'),    
    path('category',views.category,name='category'),
    path('subcategory',views.subcategory,name='subcategory'),
    path('products',views.products,name='products'),
    path('add_products',views.add_products,name='add_products'),
    
    path('profile',views.profile,name='profile'),
    path('orders',views.orders,name='orders'),
    path('order_details/<int:id>',views.orders_de,name='order_details'),
    path('cancel/<int:id>', views.cancel_order,name='cancel'),
    path('ship/<int:id>', views.ship,name='ship'),
    path('out_for_delivery/<int:id>', views.out_for_delivery,name='out_for_delivery'),
   
    path('complete/<int:id>', views.complete_order,name='complete'),
    
    path('report_date', views.report_date,name='report_date'),
    
    path('offer',views.offer,name='offer'),
    path('add_offer',views.add_offer,name='add_offer'),
    path('update_offer/<int:id>', views.update_offer,name='update_offer'),
    
    
    path('coupon_list',views.coupon_list,name='coupon_list'),
    path('coupon_disable/<int:id>',views.coupon_disable,name='coupon_disable'),
    path('coupon_edit/<int:id>',views.coupon_edit,name='coupon_edit'),
    path('coupon_add',views.coupon_add,name='coupon_add'),
    
    
    path('rep_orders',views.rep_orders,name='rep_orders'),
    path('rep_orders_yearly',views.rep_orders_yearly,name='rep_orders_yearly'),
    path('rep_products',views.rep_products,name='rep_products'),
    path('export_csv',views.export_csv,name='export_csv'),
    path('export_excel',views.export_excel,name='export_excel'),
    path('export_pdf',views.export_pdf,name='export_pdf'),
    
    path('shipping',views.profile,name='shipping'),
    path('add_cat',views.add_cate),
    path('add_subcat',views.add_subcate),
    path('', views.login,name='login'),
    path('home', views.home,name='home'),
    path('logout', views.logout)
    
]