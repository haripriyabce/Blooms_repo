from django.urls import path
from .import views
urlpatterns = [
    path('',views.index1,name='index1'), 
    path('otp_verification/<int:Phone_number>/', views.otp_verification, name='otp_verification'), 
    path('login_user', views.login,name='login_user'),
    path('login_otp/', views.login_otp,name='login_otp'),
    path('logout/', views.logout,name='logout'),    
    path('reg/', views.register,name='reg'),    
    path('us_products', views.products,name='us_products'),
    path('us_products/<int:cat>/', views.products,name='us_products'),
    path('us_products/<int:cat>/<int:sub>/', views.products,name='us_products'),    
    path('det/<int:id>', views.product_det,name='det'),   
   
    path('logout', views.logout,name='logout')
    
]