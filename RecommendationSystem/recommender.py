from django.db import connection

movieGenreList = ["action", "adventure", "animation", "children's", "comedy", "crime", "documentary", "drama", "fantasy", "film-noir", "horror", "musical", "mystery", "romance", "sci-fy", "thriller", "war", "western"]


def get_genres(ids):
    genres = []
    with connection.cursor() as cursor:
        for i in range(len(ids)):
            cursor.execute("SELECT name FROM genres WHERE id = %s", [ids[i]])
            data = cursor.fetchone()
            genres.append(data)
        return genres


def get_movies(genres):
    movies = []
    with connection.cursor() as cursor:
        for i in range(len(genres)):
            cursor.execute("SELECT title FROM movies WHERE genres = %s limit 3", [genres[i][0]])
            data = cursor.fetchall()
            movies.append(data)
        return movies

