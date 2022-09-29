from django.urls import path
from .import views
urlpatterns = [     
    path('content',views.content,name='content'),
    path('add_content',views.add_content,name='add_content'),
    path('update_con/<int:id>', views.update_content,name='update_con'),
    path('deactivate/<int:id>', views.deactivate_content),
]