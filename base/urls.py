from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #Login
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    # Other URL patterns
    # path('reset-password/', auth_views.PasswordResetView.as_view(template_name='base/password_reset.html'), name='password_reset'),
    # path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_done.html'), name='password_reset_done'),
    # path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'), name='password_reset_complete'),

   # Read
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    # Room
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    # USER
    path('update-user/', views.updateUser, name="update-user"),
    path('delete-user/', views.deleteUser, name='delete-user'),

    # Topics
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('cities/', views.cityPage, name="cities"),
 
]