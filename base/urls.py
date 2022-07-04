from unicodedata import name
from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Loginpage.as_view(), name='login'),
    path('register/', views.Registerpage.as_view(), name='register'),
    path('logout/', views.logoutPage, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forgot-password/', views.forgotPassword, name='forgot_password'),
    path('reset_password/<uidb64>/<token>', views.resetPassword, name='reset_password'),
    path('article/<str:title>/', views.Articlepage.as_view(), name='article'),
    path('user_profile/<str:pk>/', views.userProfile, name='profile'),
    path('settings/', views.userSettings, name='settings'),
    path('update-password/', views.updatePassword, name='update_password'),
    path('like/', views.like, name='like'),
    path('delete/', views.deleteComment, name='delete'),
]