from django.forms import ModelForm, Textarea
from .models import User


class WatchlistForm(ModelForm):
    class Meta:
        model = User
        fields = ['watchlist']
        widgets = {
            'watchlist': Textarea(attrs={'class': 'textarea'}),
        }
