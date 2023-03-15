from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models

from rest_framework.permissions import (
    IsAdminUser,
    BasePermission,
    IsAuthenticated,
)
import os
import re
from .choices.db_choices import (
    PRIORITY_CHOICES,
    TAG_CHOICES,
    TASK_STATUS_CHOICES,
    PROJECT_TYPE,
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

    def create_superuser(self, email, password, first_name=None, last_name=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True, editable=False)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=150)
    permissions = models.ManyToManyField(
        blank=True,
        related_query_name="users",
        to="auth.permission",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "email"
    ID_FIELD = "user_id"
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Projects(models.Model):
    project = models.PositiveIntegerField(primary_key=True, editable=False)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    type = models.CharField(
        max_length=15, choices=PROJECT_TYPE, default=PROJECT_TYPE[0][1]
    )

    def __str__(self):
        return self.title


class Contributors(models.Model):
    user = models.ForeignKey(Users, on_delete=models.RESTRICT)
    project = models.ForeignKey(Projects, on_delete=models.RESTRICT)
    role = models.CharField(max_length=150)

    class Meta:
        permissions = [
            ("DELETE", "can delete"),
            ("EDIT", "can edit ticket"),
            ("CLOSE", "can close ticket"),
            ("ONLY_READ", "can only read"),
        ]


class Issues(models.Model):
    title = models.CharField(max_length=500)
    desc = models.CharField(max_length=500)
    tag = models.CharField(
        max_length=15, choices=TAG_CHOICES, default=TAG_CHOICES[2][1]
    )
    priority = models.CharField(
        max_length=15, choices=PRIORITY_CHOICES, default=PRIORITY_CHOICES[1][1]
    )
    project = models.ForeignKey(Projects, on_delete=models.RESTRICT)
    status = models.CharField(
        max_length=15, choices=TASK_STATUS_CHOICES, default=TASK_STATUS_CHOICES[0][1]
    )
    author_user = models.ForeignKey(
        Users, related_name="author", on_delete=models.RESTRICT
    )
    assignee_user = models.ForeignKey(
        Users, related_name="assignee", on_delete=models.RESTRICT
    )
    created_time = models.DateTimeField("Created Time", auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment_id = models.PositiveIntegerField(primary_key=True)
    description = models.CharField(max_length=500)
    author_user = models.ForeignKey(Users, on_delete=models.RESTRICT)
    issue = models.ForeignKey(Issues, on_delete=models.RESTRICT)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
