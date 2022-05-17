from django.urls import path
from spotcloud_test.users.api.views.users import TokenPairView, LogoutApiView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutApiView.as_view(), name='token_logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]