from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    title = models.TextField()

class Choice(models.Model):
    choice_id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(Poll, models.CASCADE, db_column='poll_id')
    description = models.TextField()

    class Meta:
        unique_together = [['poll', 'description']]

class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(Poll, models.CASCADE, db_column='poll_id')
    choice = models.ForeignKey(Choice, models.CASCADE, db_column='choice_id')
    user = models.ForeignKey(User, models.CASCADE)
    ip = models.CharField(max_length=100)

    class Meta:
        unique_together = [['poll', 'user']]



