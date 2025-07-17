from django import forms
from .models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["title", "description", "tags", "image"]  # include all you want
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),  # or forms.SelectMultiple()
        }
