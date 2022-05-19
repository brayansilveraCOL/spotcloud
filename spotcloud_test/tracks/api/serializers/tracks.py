# Import rest_framework
from rest_framework import serializers

# Django Models
from spotcloud_test.tracks.models.tracks import Tracks, Genres

# Serializers
from spotcloud_test.tracks.api.serializers.genres import GenresModelSerializer


class TracksModelSerializer(serializers.ModelSerializer):
    genres = GenresModelSerializer(read_only=True, many=True)

    class Meta:
        model = Tracks
        fields = '__all__'


class TrackCreateSerializer(serializers.ModelSerializer):
    genres = serializers.ListField()

    class Meta:
        model = Tracks
        fields = '__all__'

    def create(self, validated_data):
        list_genres_id = validated_data.pop('genres')
        track = Tracks(**validated_data)
        track.save()
        for genre_id in list_genres_id:
            genre = Genres.objects.filter(id=genre_id.get('genre_id')).first()
            if genre:
                track.genres.add(genre)
        return track
