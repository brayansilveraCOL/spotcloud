import requests
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from spotcloud_test.tracks.models import Genres, Tracks


@api_view(['GET'])
def uploadData(request):
    genres_id = []
    genres_list = []
    genres_list_unique = []
    try:
        response = requests.get('https://rss.applemarketingtools.com/api/v2/us/music/most-played/100/songs.json')
        response = response.json()
        feed = response.get('feed')
        if feed is None:
            return Response(data={'message': 'Entity Feed not match'}, status=status.HTTP_400_BAD_REQUEST)
        results = feed.get('results')
        if results is None:
            return Response(data={'message': 'Entity results not match'}, status=status.HTTP_400_BAD_REQUEST)
        if len(results) == 0:
            return Response(data={'message': 'Results not found'}, status=status.HTTP_400_BAD_REQUEST)
        for result in results:
            if result.get('genres'):
                genres = result.get('genres')
                for genre in genres:
                    genres_list.append(genre)
                    genres_id.append(genre.get('genreId'))

        unique_id_genres = list(set(genres_id))
        for obj in genres_list:
            if obj.get('genreId') in unique_id_genres:
                etl_object = {
                    "id": int(obj.get('genreId')),
                    "name": obj.get('name'),
                    "url": obj.get('url')
                }
                genres_models = Genres(**etl_object)
                genres_models.save()
                genres_list_unique.append(genres_models)
                index_ = unique_id_genres.index(obj.get('genreId'))
                unique_id_genres.pop(index_)
        for result in results:
            etl_object = {
                "artistName": result.get('artistName'),
                "id": int(result.get('id')),
                "name": result.get('name'),
                "releaseDate": datetime.strptime(result.get('releaseDate'), '%Y-%m-%d'),
                "kind": result.get('kind'),
                "artistId": int(result.get('artistId')),
                "artistUrl": result.get('artistUrl'),
                "contentAdvisoryRating": result.get('contentAdvisoryRating'),
                "artworkUrl100": result.get('artworkUrl100'),
                "url": result.get('url'),
            }
            track = Tracks(**etl_object)
            track.save()
            if result.get('genres'):
                genres = result.get('genres')
                for genre in genres:
                    genres = Genres.objects.get(id=int(genre.get('genreId')))
                    print(genres)
                    track.genres.add(genres)

        return Response(data={'upload': True}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(data={'upload': False, 'message': e.args}, status=status.HTTP_400_BAD_REQUEST)
