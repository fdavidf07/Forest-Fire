import uuid
from django.db import models

class Simulation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.IntegerField()
    p = models.FloatField()
    f = models.FloatField()
    grid = models.JSONField() 
    steps_count = models.PositiveIntegerField(default=0)
    tree_density = models.FloatField(default=0.0)
    fire_size_history = models.JSONField(default=dict) # Para la ley de potencia