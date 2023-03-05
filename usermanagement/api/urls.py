from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user-register/', views.user_register, name='user-register'),
    path('all-user/', views.all_user, name='all-user'),
    path('view-user/', views.view_user, name='api-view-user'),
    path('user-profile/', views.user_profile, name='api-user-profile'),
    path('delete-profile/', views.delete_profile, name='api-delete-profile'),
    path('delete-any-user/<int:id>/', views.delete_any_user, name='delete-any-user'),

]