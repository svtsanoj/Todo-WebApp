from django.db import models
from django.contrib.auth.models import User

# Create your models here.
priorities = ((1, 'High'), (2, 'Medium'), (3, 'Low'))
class Todo(models.Model):
    text = models.CharField(max_length=40, unique=True)
    complete = models.BooleanField(default=False)
    priority = models.IntegerField(choices=priorities, default=3)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)