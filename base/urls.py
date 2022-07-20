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
    path('reset-password/<uidb64>/<token>', views.resetPassword, name='reset_password'),
    path('article/<str:title>/', views.Articlepage.as_view(), name='article'),
    path('user-profile/<str:pk>/', views.userProfile, name='profile'),
    path('settings/', views.userSettings, name='settings'),
    path('update-password/', views.updatePassword, name='update_password'),
    path('like/', views.like, name='like'),
    path('delete/', views.deleteComment, name='delete'),
    path('create-article/', views.createArticle, name='create-article'),
    path('article/update-article/<str:title>/', views.updateArticle, name='update-article'),
    path('article/delete-article/<str:title>/', views.deletePost, name='delete-article'),
]