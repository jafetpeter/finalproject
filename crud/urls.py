
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_create, name='add_user'),
    path('users/edit/<int:pk>/', views.user_update, name='edit_user'),
    path('users/delete/<int:pk>/', views.user_delete, name='delete_user'),
    path('users/change-password/<int:pk>/', views.change_password, name='change_password'),  # New route

    path('shifts/', views.shift_list, name='shift_list'),
    path('shifts/add/', views.shift_create, name='shift_create'),
    path('shifts/edit/<int:pk>/', views.shift_update, name='shift_update'),
    path('shifts/delete/<int:pk>/', views.shift_delete, name='shift_delete'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
]
