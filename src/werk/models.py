from django.db import models
from django.contrib.auth.models import User


class WerkUser(User):
    """
        Werk's User Model
    """
    pass


class WerkTask(models.Model):
    """
        Werk's Task Model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=30)
    body = models.TextField()
    done = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    start_time = models.DateField(null=True)
    end = models.DateField(null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)