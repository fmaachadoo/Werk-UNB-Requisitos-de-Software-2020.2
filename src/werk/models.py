from django.db import models
from django.contrib.auth.models import User


class Workspace(models.Model):
    """
        User's Workspace models
    """
    title = models.CharField(max_length=100, default='Workspace')


class Activity(models.Model):
    """
        User's activity model
    """
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)


class WerkUser(User):
    """
        Werk's User Model
    """
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    archived_workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE, primary_key=True,
                                              related_name='archived')


class WerkTask(models.Model):
    """
        Werk's Task Model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=30)
    body = models.TextField()
    done = models.BooleanField(default=False)
    start_time = models.DateField(null=True)
    end = models.DateField(null=True)