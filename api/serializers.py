"""import """
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Comments, Contributors, Issues, Projects, Users
from .validators.check_data import CheckPasswordPolicy


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Users.objects.all())])

    class Meta:
        model = Users
        fields = ("email", "password", "password2", "first_name", "last_name")

    def create(self, validated_data):
        user = Users(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        CheckPasswordPolicy().validate(password=password, password2=password2)
        user.set_password(password)
        user.save()

        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = (
            "title",
            "description",
            "type",
            "project",
            "author_user_id",
        )

        read_only_fields = (
            "project",
            "author_user_id",
        )

    def create(self, validated_data):
        author_user_id = self.context.get("request", None).user
        project = Projects(
            title=validated_data["title"],
            description=validated_data["description"],
            type=validated_data["type"],
            author_user=author_user_id,
        )
        project.save()
        Contributors(project_id=project.project, user_id=author_user_id.user_id).save()
        return project


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ("project", "user")

        read_only_fields = ("id",)


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = (
            "title",
            "desc",
            "tag",
            "priority",
            "status",
            "assignee_user",
            "id",
        )

        read_only_fields = ("id",)

    def get_project_id(self):
        return Projects(project=self.context.get("request").parser_context.get("kwargs").get("project_pk"))

    def create(self, validated_data):
        author_user_id = self.context.get("request", None).user
        issue = Issues(
            title=self.validated_data["title"],
            desc=self.validated_data["desc"],
            tag=self.validated_data["tag"],
            priority=self.validated_data["priority"],
            status=self.validated_data["status"],
            assignee_user=self.validated_data["assignee_user"],
            author_user=author_user_id,
            project=self.get_project_id(),
        )
        issue.save()
        return issue


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            "description",
            "comment_id",
        )
        read_only_fields = ("comment_id",)

    def get_issue_id(self):
        return Issues(id=self.context.get("request").parser_context.get("kwargs").get("issue_pk"))

    def create(self, validated_data):
        author_user_id = self.context.get("request", None).user
        comment = Comments(
            description=validated_data["description"],
            author_user=author_user_id,
            issue=self.get_issue_id(),
        )
        comment.save()
        return comment


class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Users
        fields = ["email", "password"]


class MyTokenObtainSerializer(TokenObtainSerializer):
    username_field = Users.USERNAME_FIELD

    class Meta:
        model = Users
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super(MyTokenObtainSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.EmailField()
        self.fields["password"] = serializers.CharField()

    def validate(self, attrs):
        self.user = Users.objects.filter(email=attrs[self.username_field]).first()

        if not self.user:
            raise serializers.ValidationError("The user is not valid.")

        if self.user:
            if not self.user.check_password(attrs["password"]):
                raise serializers.ValidationError("Incorrect credentials.")
        if self.user is None or not self.user.is_active:
            raise serializers.ValidationError("No active account found with the given credentials")

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError("Must implement `get_token` method for `MyTokenObtainSerializer` subclasses")


class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
