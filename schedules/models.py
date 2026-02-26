from django.db import models

# スケージュール
class Schedule(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='schedules')
    detail = models.CharField(max_length=255) # スケージュール詳細
    result = models.CharField(max_length=255,blank=True) # 結果
    status = models.PositiveIntegerField(default = 0) # 進捗ステータス
    order = models.PositiveIntegerField(default = 0) # 順序

    class Meta:
        # 順序が低い順（1, 2, 2, 3...）に並べる
        ordering = ['order']
        # 「event」と「order」のペアで重複を禁止する
        unique_together = ('event', 'order')

    def __str__(self):
        return f"{self.event.name} - {self.detail} (順序: {self.order})"
