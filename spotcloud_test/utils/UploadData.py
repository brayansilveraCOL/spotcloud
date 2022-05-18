import requests
from spotcloud_test.tracks.models.tracks import Genres


def uploadDataToDataBase():
    genres_id = []
    genres_list = []
    genres_list_unique = []
    response = requests.get('https://rss.applemarketingtools.com/api/v2/us/music/most-played/100/songs.json')
    response = response.json()
    feed = response.get('feed')
    if feed is None:
        raise Exception('Entity Feed not match')
    results = feed.get('results')
    if results is None:
        raise Exception('Entity results not match')
    if len(results) == 0:
        raise Exception('Results not found')

    for result in results:
        if result.get('genres'):
            genres = result.get('genres')
            for genre in genres:
                genres_list.append(genre)
                genres_id.append(genre.get('genreId'))

    unique_id_genres = list(set(genres_id))
    for obj in genres_list:
        if obj.get('genreId') in unique_id_genres:
            genres_models = Genres(**obj)
            genres_list_unique.append(genres_models)
            index_ = unique_id_genres.index(obj.get('genreId'))
            unique_id_genres.pop(index_)

    print(genres_list_unique)


uploadDataToDataBase()
