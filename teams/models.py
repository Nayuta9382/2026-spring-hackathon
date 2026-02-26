from django.db import models

# チームグループ
class TeamGroup(models.Model):
    tournament = models.ForeignKey('tournaments.Tournament', on_delete=models.CASCADE, related_name='team_groups')
    category = models.PositiveIntegerField(default = 0) # チームステータス区分
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.tournament.name} - {self.category}"


# チーム
class Team(models.Model):
    name = models.CharField(max_length=255)
    team_group = models.ForeignKey(TeamGroup, on_delete=models.CASCADE, related_name='team')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
