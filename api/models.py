import os

from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.db import models

from .choices.db_choices import (
    PRIORITY_CHOICES,
    PROJECT_CHOICES,
    STATUS_CHOICES,
    TAG_CHOICES,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name=None, last_name=None):
        if not email:
            raise ValueError("Vous devez entrer une adresse email.")

        users = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        users.set_password(password)
        users.save(user=self._db)
        return users

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


# https://thinkster.io/tutorials/django-json-api/authentication
class Users(AbstractUser):
    user_id = models.AutoField(primary_key=True, editable=False)

    email = models.EmailField(blank=False, unique=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


class Projects(models.Model):
    project = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=15, choices=PROJECT_CHOICES)
    author_user = models.ForeignKey(
        Users, related_name="project_created_by", on_delete=models.RESTRICT
    )

    def __str__(self):
        return self.title


class Contributors(models.Model):
    user = models.ForeignKey(
        Users, related_name="user_contributor", on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Projects, related_name="project_contributor", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"project: {self.project}, {self.user}"


class Issues(models.Model):
    title = models.CharField(max_length=100, blank=False)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=15, choices=TAG_CHOICES)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    author_user = models.ForeignKey(
        Users, related_name="issue_author", on_delete=models.RESTRICT
    )
    assignee_user = models.ForeignKey(
        Users, related_name="issue_assigned_to", on_delete=models.RESTRICT
    )
    created_time = models.DateTimeField("Created Time", auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True, editable=False)
    description = models.CharField(max_length=500)
    author_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)

    def __str__(self):
        return self.description
