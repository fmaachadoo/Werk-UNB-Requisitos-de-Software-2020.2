from django.db import models
from django import forms
from django.contrib.auth.models import User
from datetime import datetime


class WerkUser(User):
    """
        Werk's User Model
    """
    nickname = models.CharField(max_length=254, blank=True, null=True)


class WerkTask(models.Model):
    """
        Werk's Task Model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=800)
    done = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    start_time = models.DateField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    # Reformat the time duration
    def taskTime(self):
        sec = self.duration.total_seconds()
        if sec < 60:
            return '%01dseg' % int(sec)
        elif sec < 3600:
            return '%01dmin' % int((sec / 60) % 60)
        return '%01dh%01dmin' % (int((sec / 3600) % 3600), int((sec / 60) % 60))
