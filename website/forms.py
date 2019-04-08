from django import forms
from .models import UserPreferences

class GenreChoiceForm(forms.ModelForm):
    genre_choice = forms.BooleanField()

    class Meta:
        model = UserPreferences
        fields = ['genre_one_id', 'genre_two_id', 'genre_three_id' ]