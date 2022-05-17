from rest_framework_simplejwt.views import TokenObtainPairView

from spotcloud_test.users.api.serializers.users import TokenSerializer


class TokenPairView(TokenObtainPairView):
    serializer_class = TokenSerializer
