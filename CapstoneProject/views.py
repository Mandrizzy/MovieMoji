from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection


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

