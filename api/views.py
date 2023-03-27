from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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

    def list(self, request, project_pk=None):
        queryset = Contributors.objects.filter(project_id=project_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)


class IssueViewset(viewsets.ViewSet):
    serializer_class = IssueSerializer
    authorization_classes = []
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Issues.objects.all()


class CommentViewset(viewsets.ViewSet):
    serializer_class = CommentSerializer
    authorization_classes = []
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Comments.objects.all()

    def list(self, request):
        print(request.user)
        queryset = Projects.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        queryset = Comments()
        serializer = CommentSerializer(self.queryset, many=False)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        contrib = Contributors.objects.filter(user_id=request.user.user_id).values('project_id')
        queryset = Projects.objects.all(project_id__in=contrib)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        pass
