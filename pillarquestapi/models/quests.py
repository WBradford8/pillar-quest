from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Quest(models.Model):

    quest_title = models.CharField(max_length=50)
    quest_objective = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=CASCADE)
    pillars = models.ManyToManyField("Pillars", through="QuestPillar", related_name="CompletedQuests")
    
    