from django.db import connection

# Import Third Party Library
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from spotcloud_test.tracks.api.serializers.tracks import TracksModelSerializer, TrackCreateSerializer

# Django Models
from spotcloud_test.tracks.models.tracks import Tracks

# Utils
from spotcloud_test.utils.miscelanea import create_object


class TrackViewSet(mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = TracksModelSerializer
    queryset = Tracks.objects.filter(is_active=True)
    lookup_field = 'unique_code'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'id', 'kind', 'contentAdvisoryRating']

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def perform_destroy(self, instance):
        """Disable State."""
        instance.is_active = False
        instance.save()

    @action(detail=False, methods=['get'])
    def fifty_popularity(self, request):
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM tracks_tracks where is_active = true Limit 50''')
        row = cursor.fetchall()
        columnNames = list(map(lambda x: x[0], cursor.description))
        response = None
        response_list = []
        for obj in row:
            genres_list = []
            obj = list(obj)
            response = dict(zip(columnNames, obj))
            cursor.execute("SELECT * FROM tracks_tracks_genres where tracks_id={}".format(response.get('id')))
            tracks_tracks_genres = cursor.fetchall()
            column_names_genres_tracks = list(map(lambda x: x[0], cursor.description))
            for tracks_genres in tracks_tracks_genres:
                tracks_genres = list(tracks_genres)
                response_tracks_genres = dict(zip(column_names_genres_tracks, tracks_genres))
                cursor.execute(
                    "SELECT * FROM tracks_genres where id={}".format(response_tracks_genres.get('genres_id')))
                tracks_with_genres = cursor.fetchall()
                tracks_with_genres = list(tracks_with_genres)
                column_names_genres = list(map(lambda x: x[0], cursor.description))
                response_tracks_genres = {}
                for genres in tracks_with_genres:
                    i = 0
                    for gen in list(genres):
                        response_tracks_genres[column_names_genres[i]] = gen
                        i = i + 1
                genres_list.append(response_tracks_genres)
            response['genres'] = genres_list
            response_list.append(response)
        return Response(data={'data': response_list, 'len': len(response_list)})

    @action(detail=False, methods=['post'])
    def create_track(self, request):
        serializer = TrackCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def group_track_for_genre(self, request):
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM tracks_tracks_genres''')
        all_genres_with_id_track = cursor.fetchall()
        columnNames = list(map(lambda x: x[0], cursor.description))
        keys = []
        inventory_of_lambdas = []
        for related in all_genres_with_id_track:
            related = list(related)
            response = dict(zip(columnNames, related))
            cursor.execute("SELECT * FROM tracks_tracks where id = {}".format(response.get('tracks_id')))
            tracks = cursor.fetchone()
            columnNamesTrack = list(map(lambda x: x[0], cursor.description))
            if tracks:
                tracks = list(tracks)
                dict_from_list = dict(zip(columnNamesTrack, tracks))
                inventory_of_lambdas.append({response.get('genres_id'): dict_from_list})

        for data in inventory_of_lambdas:
            key = list(data.keys())
            keys.append(key[0])

        object_referent = create_object(keys)

        for data in inventory_of_lambdas:
            key = list(data.keys())
            if key[0] in object_referent:
                object_referent[key[0]].append(data[key[0]])

        cursor.execute('''SELECT * FROM tracks_genres''')
        genres = cursor.fetchall()
        columnNamesGenres = list(map(lambda x: x[0], cursor.description))
        list_genres = []
        for genres_obj in genres:
            genres = list(genres_obj)
            dict_genres = dict(zip(columnNamesGenres, genres))
            list_genres.append(dict_genres)

        final_object_group = {list_genres['name']: list(object_referent.get(list_genres['id']))
                              for list_genres in list_genres if
                              list_genres['id'] in object_referent.keys()
                              }

        return Response(data={'data': final_object_group}, status=status.HTTP_201_CREATED)
