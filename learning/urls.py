from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery', views.login, name='login'),
    path('register', views.register, name='register'),
    path('add_image', views.add_image, name='add_image'),
    path('delete_image', views.delete_image, name='delete_image'),
    path('update_first_name', views.update_first_name, name='update_first_name'),
    path('logout', views.logout, name='logout'),
    path('staff_panel', views.staff_panel, name='staff_panel'),
    path('api/', views.api_overview, name='api_overview'),
    path('api/user-list/', views.user_list, name='user_list'),
    path('api/user-detail/<str:pk>/', views.user_detail, name='user_detail'),
    path('api/image-create/', views.image_create, name='image_create'),
    path('api/image-update/<str:pk>/', views.image_update, name='image_update'),
    path('api/image-delete/<str:pk>/', views.image_delete, name='image_delete'),
]