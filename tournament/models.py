from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200)
    lichess_id = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    current_season_players = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    username = models.CharField(max_length=200, unique=True)
    lichess_id = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    team = models.ForeignKey(Team, blank=False, on_delete=models.SET_NULL, null=True, related_name='players')
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    is_youngster = models.BooleanField(default=False)
    is_woman = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Tournament(models.Model):
    lichess_id = models.CharField(max_length=200, null=False, blank=False, unique=True)
    name = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    season = models.ForeignKey('Season', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class TournamentTeamResult(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.IntegerField()
    score = models.FloatField()

    def __str__(self):
        return self.tournament.name + ' - ' + self.team.name + ' results'


class TournamentPlayerResult(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    nb_games = models.IntegerField(null=True, default=0)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.player.username + ' - ' + self.tournament.name + 'results'

    class Meta:
        unique_together = ['tournament', 'player']

class Season(models.Model):
    name = models.CharField(max_length=200)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return self.name
