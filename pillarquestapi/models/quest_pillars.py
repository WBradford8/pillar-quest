from django.db import models
from django.db.models.deletion import CASCADE

class QuestPillar(models.Model):

    quest = models.ForeignKey("Quest", on_delete=CASCADE)
    pillar = models.ForeignKey("Pillars", on_delete=CASCADE)