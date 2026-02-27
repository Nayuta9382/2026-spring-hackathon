from django.db import models

class EventResult(models.Model):
    # 「競技結果」
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    rank = models.PositiveIntegerField() # その競技での順位
    point = models.IntegerField(null=True, blank=True) # スコア（点数やタイムなど）
    detail = models.TextField(max_length=2000,default='') # 詳細
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['rank']
        unique_together = ('event', 'team')

    def __str__(self):
        return f"{self.event.name} - {self.rank}位: {self.team.name}"