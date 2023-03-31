from django.contrib import admin
from api.models import Users, Contributors, Projects, Comments, Issues


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    fields = ("user_id", "is_active", "email", "fist_name", "last_name", "date_joined")

    def __str__(self):
        return "email"


@admin.register(Contributors)
class ContributorAdmin(admin.ModelAdmin):
    fields = ("project", "user")


@admin.register(Projects)
class ProjectAdmin(admin.ModelAdmin):
    fields = ("title", "description", "type", "author_user")


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    fields = ("description", "author_user", "issue", "created_time")
    readonly_fields = ("created_time",)


@admin.register(Issues)
class IssueAdmin(admin.ModelAdmin):
    fields = (
        "assignee_user",
        "author_user",
        "project",
        "desc",
        "tag",
        "priority",
        "status",
    )
    readonly_fields = ("created_time",)
