from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenBlacklistSerializer
)

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from .cryptography import AESCipher
from .status_code import Status_code
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model

aes = AESCipher(settings.SECRET_KEY[:16], 32)


#################################################################
# Custom Token Obtain Pair Serializer, to make it work add it in the SIMPLE_JWT settings in the settings.py
#################################################################

class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):

        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        print('uz ', self.user)

        if not self.user:
            return {
                'message': 'Login Failed',
                'status_code': Status_code.unauthorized

            }
        refresh = self.get_token(self.user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        data['message'] = 'Login Successful'

        return {
            'message': data['message'],
            'id': aes.encrypt(str(self.user.id)),
            'username': self.user.username,
            'email': self.user.email,
            'token': {
                'refresh': data["refresh"],
                'access': data["access"]
            }
        }


class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        try:
            refresh.blacklist()
        except AttributeError:
            pass
        return {
            "message": "Logout Successful",
            "status_code": Status_code.success
        }
