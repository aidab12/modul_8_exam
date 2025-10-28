import re
from typing import Any

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.tokens import Token, RefreshToken

from apps.models.users import User


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise ValidationError("Пользователь уже зарегестрирован.")

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

    def to_representation(self, instance):
        return {
            "user": {
                "id": instance.id,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "phone": instance.phone,
            },
            "message": "Registration successful."
        }


class SendSmsCodeSerializer(Serializer):
    phone = CharField(default='971884040')

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')

        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs):
        phone = attrs['phone']
        user, created = User.objects.get_or_create(phone=phone)
        user.set_unusable_password()

        return super().validate(attrs)


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'first_name', 'last_name', 'phone',


class VerifySmsCodeSerializer(Serializer):
    phone = CharField(default='971884040')
    code = IntegerField(default=100000)
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs: dict[str, Any]):
        self.user = authenticate(phone=attrs['phone'], request=self.context['request'])

        if self.user is None:
            raise ValidationError(self.default_error_messages['no_active_account'])

        return attrs

    @property
    def get_data(self):
        refresh = self.get_token(self.user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        user_data = UserModelSerializer(self.user).data

        return {
            'message': "OK",
            'data': {
                **data, **{'user': user_data}
            }
        }

    @classmethod
    def get_token(cls, user) -> Token:
        return cls.token_class.for_user(user)
