from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.loginPage, name='login'),
  path('logout/', views.logoutUser, name='logout'),
  path('register/', views.registerPage, name='register'),
  
  path('', views.home, name='home'), # name parameter allows for easier referencing of this path later
  path('room/<str:pk>/', views.room, name='room'),
  path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
  path('create-room/', views.createRoom, name='create-room'),
  path('update-room/<str:pk>', views.updateRoom, name='update-room'),
  path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
  path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
  path('update-user/', views.updateUser, name='update-user'),
  path('topics/', views.topicsPage, name='topics'),
  path('activities/',views.activitiesPage, name='activities')
]
