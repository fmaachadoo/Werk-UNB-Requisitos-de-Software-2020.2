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
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)


class WerkUser(User):
    """
        Werk's User Model
    """
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    archived_workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE, primary_key=True,
                                              related_name='archived')
