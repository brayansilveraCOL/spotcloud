from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenBackendError


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.email
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['email'] = str(self.user.email)
        data['username'] = str(self.user.username)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    default_error_messages = {
        'bad_token': 'Token is Expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenBackendError:
            self.fail('Bad Token')
