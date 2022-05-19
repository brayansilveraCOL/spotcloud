from django.urls import path
from spotcloud_test.tracks.api.views.upload import uploadData

urlpatterns = [
    path('v1/upload/', uploadData, name='upload_data'),
]