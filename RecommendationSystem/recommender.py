import numpy as np
import math
from django.db import connection
from django.shortcuts import render
import json



movieGenreList = ["Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]


def get_genres(ids):
    genres = []
    with connection.cursor() as cursor:
        for i in range(len(ids)):
            cursor.execute("SELECT name FROM genres WHERE id = %s", [ids[i]])
            data = cursor.fetchone()
            genres.append(data)
        return genres


def get_movie_title_from_id(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT title FROM movies WHERE movieId = %s", [id])
        movie_title = cursor.fetchone()
        return movie_title[0]


def get_movie_id_from_title(title):
    with connection.cursor() as cursor:
        cursor.execute("SELECT movieId FROM movies WHERE title = %s", [title])
        movie_title = cursor.fetchone()
        return movie_title[0]


def get_new_user_movies(request):
    user = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("SELECT genre_one_id,genre_two_id,genre_three_id FROM user_preferences WHERE user_id = %s", [user])
        row = cursor.fetchone()
        data = get_genres(row)
        movies = get_movies(data)
        jsondata = json.dumps(movies)
    return render(request, 'new_user_reccomend.html', {'movies': jsondata})


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
        return 1900
    start += 1  # skip the bracket, move to the next character
    end = movieTitle.find(')', start)
    if end == -1:
        # No closing bracket found after the opening bracket.
        # Should this be an error instead?
        return int(movieTitle[start:])
    else:
        # return int(movieTitle[start:end])
        try:
            return int(movieTitle[start:end])
        except ValueError:
            new_string = movieTitle.replace(movieTitle[start:end], '')
            new_string2 = new_string.replace('()', '')
            return extract_movie_year(new_string2)


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
    movie2 = create_movie_array("Tom and Huck (1995)")
    test = computeGenreSimilarity(movie1, movie2)
    return test


def generate_movie_candidates(movie_title):
    candidates = []
    movie_one = create_movie_array(movie_title)
    with connection.cursor() as cursor:
        cursor.execute("SELECT title FROM movies", [])
        data = cursor.fetchall()
    for i in data:
        str1 = ''.join(i)
        movie_two = create_movie_array(str1)
        try:
            if computeGenreSimilarity(movie_one, movie_two) > 0.70:
                candidates.append(i)
            else:
                continue
        except ZeroDivisionError:
            continue
    return candidates


def update_watch_movie(movieTitle, user):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(user_id) FROM user_recently_watch_movies WHERE user_id = %s", [user])
        count = cursor.fetchone()
        if count[0] != 0:
            cursor.execute("SELECT movieId FROM movies WHERE title = %s", [movieTitle])
            row = cursor.fetchone()

            cursor.execute("SELECT most_recent_movie FROM user_recently_watch_movies WHERE user_id = %s", [user])
            movieOne = cursor.fetchone()

            cursor.execute("SELECT second_most_recent_movie FROM user_recently_watch_movies WHERE user_id = %s", [user])
            movieTwo = cursor.fetchone()

            cursor.execute("UPDATE user_recently_watch_movies SET most_recent_movie = %s,"
                           " second_most_recent_movie = %s,"
                           " third_most_recent_movie = %s", [row[0], movieOne[0], movieTwo[0]])
            cursor.close()
        else:
            cursor.execute("SELECT movieId FROM movies WHERE title = %s", [movieTitle])
            row = cursor.fetchone()

            cursor.execute("INSERT INTO user_recently_watch_movies (user_id,most_recent_movie) VALUES (%s,%s)", [user, row[0]])
            cursor.close()


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
    return result


def querySet_to_list(qs):
        """
        this will return python list<dict>
        """
        return [dict(q) for q in qs]


def get_user_age(request):
    user = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("SELECT DOB FROM user_preferences WHERE user_id = %s", [user])
        data = cursor.fetchone()
        DOB = data[0]
        year = DOB[:4]
        yearInt = int(year)
        currentyear = 2019
        return currentyear - yearInt


def filter_candidates_by_age(candidates, user_age):
    new_candidates = []
    current_year = 2019
    firstcount = len(candidates)
    for i in candidates:
        release_year = extract_movie_year(i[0])
        if release_year > current_year - user_age + 12:
            new = candidates.pop(candidates.index(i))
            new_candidates.append(new)
    secondcount = len(candidates)
    return new_candidates


def filter_candidates_by_ratings(candidates):
    new_candidates = []
    for i in candidates:
        movie_id = get_movie_id_from_title(i[0])
        ratings = calculate_average_ratings(movie_id)
        if ratings >= 3:
            new = candidates.pop(candidates.index(i))
            new_candidates.append(new)
    return new_candidates


def calculate_average_ratings(movieId):
    rating = 0
    count = 0
    with connection.cursor() as cursor:
        cursor.execute("SELECT rating FROM ratings_small WHERE movieId = %s", [movieId])
        ratings = cursor.fetchall()
        for i in ratings:
            count = count + 1
            rating = rating + i[0]
        try:
            avg_ratings = int(rating / count)
            return avg_ratings
        except ZeroDivisionError:
            return 0


def get_recently_watched_movies(request):
    movies = []
    count = 0
    user = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("SELECT most_recent_movie, second_most_recent_movie, third_most_recent_movie FROM user_recently_watch_movies WHERE user_id = %s", [user])
        movie_ids = cursor.fetchone()
        if movie_ids is None:
            return movies
        for i in movie_ids:
            if i == '' or i is None:
                return movies
            title = get_movie_title_from_id(i)
            movies.append(title)
            count += 1
            if title is None:
                return movies
    return movies


