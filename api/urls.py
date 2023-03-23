from django.urls import path, include
from .views import (
    UserViewset,
    ProjectViewset,
    ContributorViewset,
    CommentViewset,
    IssueViewset,
    MyTokenObtainPairView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers


# doc : https://github.com/alanjds/drf-nested-routers

base_router = routers.DefaultRouter()
base_router.register(r'projects', ProjectViewset, basename="projects")
## generates:
# /projects/
# /projects/{pk}/
projects_router = routers.NestedSimpleRouter(base_router, r'projects', lookup='project')
projects_router.register(r'users', ContributorViewset, basename="user")
## generates:
# /projects/{project_pk}/users/
# /projects/{project_pk}/users/{contributor_pk}/
projects_router.register(r'issues', IssueViewset, basename='issues')
projects_router.register(r'users', ContributorViewset, basename="users")
issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewset, basename='comments')
## generates:
# /projects/{project_pk}/issues/
# /projects/{project_pk}/issues/{issues_pk}/
# /projects/{project_pk}/issues/{issues_pk}/comments

urlpatterns = [
    path("", include(base_router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),
    path("signup/", UserViewset.as_view({'post': 'create'}), name="signup"),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
