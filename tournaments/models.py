from django.db import models
from django.core.validators import FileExtensionValidator
import uuid

# 大会
class Tournament(models.Model):
    name = models.CharField(max_length=255)
    url_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    img_path = models.ImageField(upload_to='uploads/tournament-img/', validators=[FileExtensionValidator(['png','jpg'])],null=True,blank=True)
    password = models.CharField(max_length=255)
    status = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_img_path = models.FileField(upload_to='uploads/tournament-pdf/', validators=[FileExtensionValidator(['pdf'])],null=True,blank=True)

    class Meta:
        # 大会を作成日時が新しい順（降順）に並べる
        ordering = ['-created_at']



    def __str__(self):
        return self.name

# 大会ポイント
class TournamentPoint(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='points') # 大会の外部キー参照
    rank = models.PositiveIntegerField() # 順位
    point = models.PositiveIntegerField(default = 0) # ポイント
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        # 順序が低い順（1, 2, 2, 3...）に並べる
        ordering = ['rank']
        # 「event」と「order」のペアで重複を禁止する
        unique_together = ('tournament', 'rank')

