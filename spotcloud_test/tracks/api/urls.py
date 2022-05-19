from django.urls import path, include
from rest_framework.routers import DefaultRouter

from spotcloud_test.tracks.api.serializers.tracks import TracksModelSerializer
from spotcloud_test.tracks.api.views.upload import uploadData
from spotcloud_test.tracks.api.views.tracks import TrackViewSet
from spotcloud_test.tracks.models import Tracks

router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='tracks')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/upload/', uploadData, name='upload_data'),
]