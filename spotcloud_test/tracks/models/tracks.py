# Imports Python
import uuid

# Imports Django
from django.db import models

# Imports Utils
from spotcloud_test.utils.BaseModel import BaseModel


class Genres(BaseModel):
    unique_code = models.UUIDField('Code Unique Generate', default=uuid.uuid4, editable=False)
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField('Name Genres', max_length=255, blank=False, null=False)
    url = models.URLField("Url Genres")

    def __str__(self):
        return self.name


class Tracks(BaseModel):
    unique_code = models.UUIDField('Code Unique Generate', default=uuid.uuid4, editable=False)
    genres = models.ManyToManyField(Genres)
    artistName = models.CharField('Artist Name', max_length=255, blank=False, null=False)
    name = models.CharField('Name Track', max_length=255, blank=False, null=False)
    id = models.PositiveIntegerField('Id Track', unique=True, primary_key=True)
    releaseDate = models.DateField('Release Date')
    kind = models.CharField('Kind Name', max_length=255, blank=True, null=True)
    artistId = models.PositiveIntegerField('Artist Date')
    artistUrl = models.URLField("url Artist")
    contentAdvisoryRating = models.CharField('Content Advisors', max_length=255, blank=True, null=True)
    artworkUrl100 = models.URLField("Url Arts")
    url = models.URLField("url Track")

    def __str__(self):
        return self.name
