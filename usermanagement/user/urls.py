from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-user/<int:id>/', views.delete_user, name='delete-user'),
    path('profile/', views.profile, name='profile'),
    path('delete-profile/', views.delete_profile, name='delete-profile'),

]