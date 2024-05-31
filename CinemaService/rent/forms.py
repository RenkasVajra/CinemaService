from django import forms

MOVIE_QUANTITY_CHOICES = [(i, i) for i in range(1, 21)]


class CartAddMovieForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.Select(MOVIE_QUANTITY_CHOICES))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
