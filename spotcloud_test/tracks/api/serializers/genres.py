# Import rest_framework
from rest_framework import serializers

# Django Models
from spotcloud_test.tracks.models.tracks import Genres


class GenresModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = '__all__'
