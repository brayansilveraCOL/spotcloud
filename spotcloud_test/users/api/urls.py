from django.urls import path
from spotcloud_test.users.api.views.users import TokenPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('v1/login/', TokenPairView.as_view(), name='token_obtain_pair'),
    path('v1/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/verify/', TokenVerifyView.as_view(), name='token_verify'),
]