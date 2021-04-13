from django.db import models
from django.contrib.auth.models import User


class Workspace(models.Model):
    title = models.CharField(default='Workspace')


class Activity(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)


class WerkUser(User):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    archived_workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE, primary_key=True)
