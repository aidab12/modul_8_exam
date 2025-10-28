from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.views import (
    LoginAPIView, SendCodeAPIView, VerifySmsCodeSerializer, SignUpAPIView
)

urlpatterns = [
    path('auth/register', SignUpAPIView.as_view(), name='register'),
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login', LoginAPIView.as_view(), name='register'),
    # path('confirm-sms', VerifySmsCodeSerializer, name='register'),

]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
