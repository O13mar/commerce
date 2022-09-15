from .models import Listings
from django import forms


class listForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = [
            'title',
            'description',
            'imageurl',
            'price',
            'category'
        ]
