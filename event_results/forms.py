from django import forms
from .models import EventResult

class EventResultForm(forms.ModelForm):
    class Meta:
        model = EventResult
        fields = ['rank', 'point', 'detail']