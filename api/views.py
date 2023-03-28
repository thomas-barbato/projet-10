from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    UserSerializer,
    ProjectSerializer, ContributorSerializer, CommentSerializer, IssueSerializer,
    MyTokenObtainPairSerializer
)
from .models import Users, Projects, Issues, Comments, Contributors
from rest_framework import status, permissions
from api.models import Users

# Rest Framework imports
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewset(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = Users.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProjectViewset(ModelViewSet):
    authorization_classes = []
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_queryset(self):
        contributors = Contributors.objects.filter(user=self.request.user)
        return (Projects.objects.filter(author_user_id=self.request.user)
                | Projects.objects.filter(project_contributor__in=contributors))


class ContributorViewset(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    authorization_classes = []
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Contributors.objects.all()

    def list(self, request, **kwargs):
        queryset = Contributors.objects.filter(project_id=kwargs.get("project_pk"))
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, project_pk=None, pk=None):
        query = get_object_or_404(self.queryset, project_id=project_pk, user_id=pk)
        if query:
            query.delete()
            return Response({"delete": "success"}, status=status.HTTP_202_ACCEPTED)
        return Response({"contributor": "not found"}, status=status.HTTP_404_NOT_FOUND)


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    authorization_classes = []
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Issues.objects.all()

    def list(self, request, **kwargs):
        queryset = Issues.objects.filter(project_id=kwargs.get("project_pk"))
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, project_pk=None, pk=None):
        query = get_object_or_404(self.queryset, project_id=project_pk, id=pk)
        if query:
            query.delete()
            return Response({"delete": "success"}, status=status.HTTP_202_ACCEPTED)
        return Response({"issue": "not found"}, status=status.HTTP_404_NOT_FOUND)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authorization_classes = []
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Comments.objects.all()

    def list(self, request, **kwargs):
        queryset = Comments.objects.filter(issue_id=kwargs.get('issue_pk'))
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, project_pk=None, issue_pk=None, pk=None):
        query = get_object_or_404(self.queryset, issue_id=issue_pk, comment_id=pk)
        if query:
            query.delete()
            return Response({"delete": "success"}, status=status.HTTP_202_ACCEPTED)
        return Response({"issue": "not found"}, status=status.HTTP_404_NOT_FOUND)
