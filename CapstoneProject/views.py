from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from RecommendationSystem import recommender


def index(request):
    return render(request, "landing.html", {})


@login_required
def home(request):
    return render(request, "dashboard.html", {})


@login_required
def setup(request):
    if request.method == 'GET':
        return render(request, "setup.html", {})
    elif request.method == 'POST':
        data = request.POST.getlist('genre')
        genreOne = data[0]
        genreTwo = data[1]
        genreThree = data[2]
        user = request.user.id
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO user_preferences (user_id, genre_one_id, genre_two_id, genre_three_id) VALUES (%s, %s, %s, %s)",[user, genreOne, genreTwo, genreThree])
            cursor.close()
        return redirect('home')


@login_required
def recommend(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT genre_one_id,genre_two_id,genre_three_id FROM user_preferences WHERE user_id = %s", [request.user.id])
        row = cursor.fetchone()
        data = recommender.get_genres(row)
        movies = recommender.get_movies(data)
        # return HttpResponse(movies)
    # return HttpResponse(row)
    return render(request, 'reccomend.html', {'movies': movies})


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
    [genre]= recommender.get_genres_from_movie_title(title)
    year=recommender.extract_movie_year(title)

    #return HttpResponse(genre)
    return render(request,'watching.html',{'title':title,'genre':genre,'year':year})