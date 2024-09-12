from typing import AbstractSet

from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=50)
    credit = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return self.name
