from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from users.models import movies
from RecommendationSystem import recommender
import json


def index(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {})
    else:
        return redirect(home)


@login_required
def home(request):
    return render(request, "dashboard.html", {})


@login_required
def setup(request):
    if request.method == 'GET':
        return render(request, "setup.html", {})
    elif request.method == 'POST':
        data = request.POST.getlist('genre')
        DOB = request.POST.get('DOB')
        genreOne = data[0]
        genreTwo = data[1]
        genreThree = data[2]
        user = request.user.id
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO user_preferences (user_id, genre_one_id, genre_two_id, genre_three_id, DOB) VALUES (%s, %s, %s, %s, %s)",[user, genreOne, genreTwo, genreThree, DOB])
            cursor.close()
        return redirect('home')


@login_required
def recommend(request):
    user = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(user_id) FROM user_recently_watch_movies WHERE user_id = %s", [user])
        count = cursor.fetchone()
        if count[0] != 0:
            cursor.execute("SELECT most_recent_movie FROM user_recently_watch_movies WHERE user_id = %s", [user])
            movie = cursor.fetchone()
            movie_title = recommender.get_movie_title_from_id(movie[0])
            movies_list = recommender.generate_movie_candidates(movie_title)
            user_age = recommender.get_user_age(request)
            first_filter = recommender.filter_candidates_by_age(movies_list, user_age)
            second_filter = recommender.filter_candidates_by_ratings(first_filter)
            jsondata = json.dumps(second_filter)
            return render(request, 'reccomend.html', {'movies': jsondata})
        else:
            return recommender.get_new_user_movies(request)


@login_required
def watch(request):
    # test = recommender.plotMatrix("Toy Story (1995)")

    # test = recommender.create_movie_array("Toy Story (1995)")

    # test = recommender.test()
    test = recommender.generate_movie_candidates("Toy Story (1995)")

    return HttpResponse(test)
    # return render(request, 'watching.html', {})


@login_required
def watching(request, title):
    if request.method == 'GET':
        [genre] = recommender.get_genres_from_movie_title(title)
        year = recommender.extract_movie_year(title)
        return render(request, 'watching.html', {'title': title, 'genre': genre, 'year': year})
    elif request.method == 'POST':
        user = request.user.id
        recommender.update_watch_movie(title, user)
        return redirect('home')


@login_required
def stop(request, title):
    if request.method == 'POST':
        return HttpResponse('yes')


def watched(request):
    if request.method == 'GET':
        return render(request, 'watched.html', {})

        # return HttpResponse('yes')


@login_required
def later(request, title):
    if request.method == 'POST':
        return HttpResponse('yes')
    #return HttpResponse(genre)
    return render(request,'watching.html',{'title':title,'genre':genre,'year':year})


@login_required
def search(request):
    if request.method == 'POST':
        data = request.POST.get('search')
        result = movies.objects.filter(title__icontains=data).values()
        result2 = recommender.querySet_to_list(result) # python list return.(json-able)
    return render(request,'search.html',{'movies':result2})
