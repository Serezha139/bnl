from django.db import models
from enum import Enum
from tournament.models import Player, Tournament
# Create your models here.

class GameResult(Enum):
    black_win = 'black_win'
    white_win = 'white_win'
    draw = 'draw'

class Game(models.Model):
    player_white = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_white')
    player_black = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_black')
    team_white = models.ForeignKey('tournament.Team', on_delete=models.CASCADE, related_name='team_white', null=True, blank=True)
    team_black = models.ForeignKey('tournament.Team', on_delete=models.CASCADE, related_name='team_black', null=True, blank=True)
    elo_white = models.IntegerField(null=True, blank=True)
    elo_black = models.IntegerField(null=True, blank=True)
    elo_white_change = models.IntegerField(null=True, blank=True)
    elo_black_change = models.IntegerField(null=True, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    result = models.CharField(max_length=200, null=True, blank=True, choices=[(tag, tag.value) for tag in GameResult])
    opening = models.CharField(max_length=200, null=True, blank=True)
    moves = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)