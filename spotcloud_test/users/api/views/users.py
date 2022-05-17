from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from spotcloud_test.users.api.serializers.users import LogoutSerializer, TokenSerializer


class TokenPairView(TokenObtainPairView):
    serializer_class = TokenSerializer


class LogoutApiView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)