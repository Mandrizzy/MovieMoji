from django.db import models


class watched_movies(models.Model):
    user_id = models.IntegerField(),
    most_recently_watched = models.IntegerField(),
    second_most_recently_watched = models.IntegerField(),
    third_recently_watched = models.IntegerField(),

