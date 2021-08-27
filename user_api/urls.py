from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import path, include

from .views import email_verified, GetUserView

urlpatterns = [
    path('auth/password/reset/confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('auth/registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('email-verified', email_verified),
    path('user/<int:pk>', GetUserView.as_view()),
]
