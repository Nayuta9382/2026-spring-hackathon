from django import forms
from .models import Tournament


class CreateForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'img_path', 'password', 'pdf_img_path']
        widgets = {
            'img_path': forms.FileInput(attrs={
                'accept': 'image/png, image/jpeg, image/jpg', 
            }),
            'pdf_img_path': forms.FileInput(attrs={
                'accept': '.pdf, application/pdf', 
            }),
        }
    # 順位とポイントのバリデーション
    def clean(self):
        cleaned_data = super().clean()
        raw_teams = self.data.getlist('teams')
        raw_points = self.data.getlist('rank_points')
        cleaned_data = super().clean()
        raw_teams = self.data.getlist('teams')
        raw_points = self.data.getlist('rank_points')

        teams = [t.strip() for t in raw_teams if t.strip()]
        points_str = [p.strip() if p.strip() else "0" for p in raw_points]

        # 検証ロジック
        if not teams:
            raise forms.ValidationError("チーム名を1つ以上入力してください。")

        if len(teams) != len(points_str):
            raise forms.ValidationError(f"チーム数({len(teams)})とポイント数({len(points_str)})が一致しません。")

        try:
            points = [int(p) for p in points_str]
        except ValueError:
            raise forms.ValidationError("ポイントには数字を入力してください。")

        # Serviceに渡すために整理
        cleaned_data['team_names'] = teams
        cleaned_data['points'] = points
        return cleaned_data

#大会ステータスpulldwon
class UpdateStatusForm(forms.ModelForm):
    STATUS_CHOICES = [
        (0, '開催前'),
        (1, '開催中'),
        (2, '終了'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select,
        label="大会ステータス"
    )

    class Meta:
        model = Tournament
        fields = ['status']
