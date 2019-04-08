from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GenreChoiceForm

def index(request):
   return render(request, "landing.html", {})

@login_required
def dashboard(request):
   return render(request, "dashboard.html", {})

def setup(request):
      return render(request, "setup.html", {})

@login_required
def post(request):
    if request.method == 'POST':
        form = GenreChoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('dashboard')
    else:
        form = GenreChoiceForm()
    return render(request, 'setup.html', {'form': form})
