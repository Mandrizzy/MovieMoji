from django.db import models

# Create your models here.

class movies(models.Model):
    movieId=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=200)
    genres=models.CharField(max_length=200)

    class Meta:
        db_table = 'movies'

    def __str__(self):
        return self.title

    

