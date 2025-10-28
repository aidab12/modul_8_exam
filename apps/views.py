from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.serializers import (
    SendSmsCodeSerializer, VerifySmsCodeSerializer, SignUpSerializer
)
from apps.utils import random_code, send_sms_code, check_sms_code


@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        tags=['Аутентификация/Авторизация']
    )
)
class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = AllowAny,


class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random_code()
        phone = serializer.data['phone']
        send_sms_code(phone, code)
        return Response({"message": "send sms code"})


class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = check_sms_code(**serializer.data)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)
