from django.db import models

# スケジュール
class Schedule(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='schedules')
    detail = models.CharField(max_length=255) # スケジュール詳細
    result = models.CharField(max_length=255,blank=True) # 結果
    status = models.PositiveIntegerField(default = 0) # 進捗ステータス
    order = models.PositiveIntegerField(default = 0) # 順序

    class Meta:
        # 順序が低い順に並べる
        ordering = ['order']
        unique_together = ('event', 'status', 'order')

    def __str__(self):
        return f"{self.event.name} - {self.detail} (ステータス: {self.status}, 順序: {self.order})"
