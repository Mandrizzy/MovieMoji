from django.db import models

# Create your models here.

class UserPreferences(models.Model):
    genre_one_id = models.BooleanField(default=True)
    genre_two_id = models.BooleanField(default=True)
    genre_three_id = models.BooleanField(default=True)
