from django.db import models

# 競技
class Event(models.Model):
    tournament = models.ForeignKey('tournaments.Tournament', on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=255) # 競技名
    category = models.PositiveIntegerField(default=0) # 競技区分
    team_group = models.ForeignKey('teams.TeamGroup', on_delete=models.CASCADE, related_name='team_events') # チームグループID
    detail = models.TextField(max_length=2000, default='',blank=True) # 競技詳細
    tournament_img = models.ImageField(upload_to='tournaments/', null=True, blank=True) #トーナメント画像
    event_img = models.ImageField(upload_to='events/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # クラスポイントを使用したかどうか
    is_class_point = models.BooleanField(
        default=False, 
        verbose_name="クラスポイント対象",
        blank=True  # フォームで必須入力にしない
    )
    
    def __str__(self):
        return f"{self.tournament.name} - {self.name}"
