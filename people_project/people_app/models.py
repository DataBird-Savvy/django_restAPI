from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    def __str__(self):
        return self.team_name

class People(models.Model):
    team=models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members',null=True, blank=True,default=None)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
