from django.db import models
from django.urls import reverse
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

class Users(models.Model):
    user = models.IntegerField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    password = models.CharField(max_length=500)

class Projects(models.Model):
    project = models.IntegerField(primary_key=True, editable=False)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=500)
    author_user = models.ForeignKey(Users, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title

class Issues(models.Model):
    title = models.CharField(max_length=500)
    desc = models.CharField(max_length=500)
    tag = models.CharField(max_length=500)
    priority = models.CharField(max_length=500)
    project = models.ForeignKey(Projects, on_delete=models.RESTRICT)
    status = models.CharField(max_length=500)
    author_user = models.ForeignKey(Users, related_name="author", on_delete=models.RESTRICT)
    assignee_user = models.ForeignKey(Users, related_name="assignee", on_delete=models.RESTRICT)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    comment = models.IntegerField(primary_key=True, editable=False)
    description = models.CharField(max_length=500)
    author_user = models.ForeignKey(Users, on_delete=models.RESTRICT)
    issue = models.ForeignKey(Issues, on_delete=models.RESTRICT)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
