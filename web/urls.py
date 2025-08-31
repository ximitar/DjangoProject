from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('registration/', views.registartion_view, name='registration'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('create_room/', views.create_room, name='create_room'),
    path('room_list/', views.room_list, name='room_list'),
    path('room_det/<int:room_id>/', views.room_detail, name='room_detail'),
    path('join_room_from_list/', views.join_room_from_list,
         name='join_room_from_list'),
]
