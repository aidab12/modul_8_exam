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

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        code = random_code()
        phone = user.phone
        send_sms_code(phone, code)

        return Response(
            serializer.to_representation(user),
            status=status.HTTP_201_CREATED
        )

@extend_schema_view(
    post=extend_schema(
        summary='Отправка SMS кода',
        tags=['Аутентификация/Авторизация']
    )
)
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random_code()
        phone = serializer.data['phone']
        send_sms_code(phone, code)
        return Response({"message": "send sms code"})


@extend_schema_view(
    post=extend_schema(
        summary='Подтверждение кода и активация аккаунта',
        tags=['Аутентификация/Авторизация']
    )
)
class VerifyCodeAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = check_sms_code(
            phone=serializer.validated_data['phone'],
            code=serializer.validated_data['code']
        )

        if not is_valid_code:
            return Response(
                {"message": "Invalid verification code"},
                status=status.HTTP_400_BAD_REQUEST
            )


        serializer.activate_user()

        return Response(serializer.get_data, status=status.HTTP_200_OK)