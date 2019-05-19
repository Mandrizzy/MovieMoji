import numpy as np
import math
from django.db import connection

movieGenreList = ["Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]


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


def get_genres_from_movie_title(movieTitle):
    with connection.cursor() as cursor:
        cursor.execute("SELECT genres FROM movies WHERE title = %s", [movieTitle])
        data = cursor.fetchone()
        return data

def extract_movie_year(movieTitle):
    start = movieTitle.find('(')
    if start == -1:
        # No opening bracket found. Should this be an error?
        return ''
    start += 1  # skip the bracket, move to the next character
    end = movieTitle.find(')', start)
    if end == -1:
        # No closing bracket found after the opening bracket.
        # Should this be an error instead?
        return int(movieTitle[start:])
    else:
        return int(movieTitle[start:end])


def if_genre_exists(x, y):
    cleaned = y.split('|')
    print(str(cleaned))
    if x in y:
        return True
    else:
        return False


def create_movie_array(movieTitle):
    count = 1
    movieArray = np.array([movieTitle, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    genres = get_genres_from_movie_title(movieTitle)
    for i in movieGenreList:
        if if_genre_exists(i, genres[0]):
            movieArray[count] = 1
        count += 1
    movie = movieArray
    return movie


def test():
    movie1 = create_movie_array("Toy Story (1995)")
    # movie2 = create_movie_array("GoldenEye (1995)")
    movie2 = create_movie_array("Tom and Huck (1995)")
    test = computeGenreSimilarity(movie1, movie2)
    return test


def generate_movie_candidates(movie_title):
    candidates = []
    movie_one = create_movie_array(movie_title)
    with connection.cursor() as cursor:
        cursor.execute("SELECT title FROM movies", [])
        data = cursor.fetchall()
        # return data
    for i in data:
        # return type(i)
        str1 = ''.join(i)
        # return str1
        movie_two = create_movie_array(str1)
        try:
            if computeGenreSimilarity(movie_one, movie_two) > 0.50:
                candidates.append(i)
            else:
                continue
        except ZeroDivisionError:
            continue
    return candidates



def computeGenreSimilarity(movieOne, movieTwo):
    count = 0
    genres1 = np.delete(movieOne, 0)
    genres2 = np.delete(movieTwo, 0)
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(genres1)):
        x = int(genres1[i])
        y = int(genres2[i])
        sumxx = sumxx + (x*x)
        sumyy = sumyy + (y*y)
        sumxy = sumxy + (x*y)
        count = count + 1
    result = sumxy/math.sqrt(sumxx*sumyy)
    # print(result)
    return result

def querySet_to_list(qs):
        """
        this will return python list<dict>
        """
        return [dict(q) for q in qs]