from django import forms
from .models import Event

class CreateForm(forms.ModelForm):
    teams = forms.CharField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Event
        fields = ['name', 'category', 'detail', 'tournament_img', 'event_img']


    # teamsの値を取得
    def clean_teams(self):
        raw_teams = self.data.getlist('teams')
        # 2. 空文字（スペース含む）を除去
        filtered_teams = [name.strip() for name in raw_teams if name.strip()]
        return filtered_teams