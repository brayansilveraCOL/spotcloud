import requests
import os


def uploadDataToDataBase():
    response = requests.get('https://rss.applemarketingtools.com/api/v2/us/music/most-played/100/songs.json')

