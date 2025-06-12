from django.urls import path
from .views import (UserCreateView, UserDetailView,
                    PasswordChangeView, PasswordResetRequestView, PasswordResetConfirmView)

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('me/set-password/', PasswordChangeView.as_view(),
         name='user-set-password'),
    path('password-reset/', PasswordResetRequestView.as_view(),
         name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
]
