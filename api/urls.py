from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (CommentViewset, ContributorViewset, IssueViewset,
                    MyTokenObtainPairView, ProjectViewset, UserViewset)

# /projects/
# /projects/{pk}/
base_router = routers.DefaultRouter()
base_router.register(r"projects", ProjectViewset, basename="projects")
# /projects/{project_pk}/users/
# /projects/{project_pk}/users/{contributor_pk}/
projects_router = routers.NestedSimpleRouter(base_router, r"projects", lookup="project")
users_router = routers.NestedSimpleRouter(base_router, r"projects", lookup="user")
projects_router.register(r"users", ContributorViewset)
# /projects/{project_pk}/issues/
# /projects/{project_pk}/issues/{issues_pk}/
# /projects/{project_pk}/issues/{issues_pk}/comments
projects_router.register(r"issues", IssueViewset)
issues_router = routers.NestedSimpleRouter(projects_router, r"issues", lookup="issue")
issues_router.register(r"comments", CommentViewset, basename="comments")

urlpatterns = [
    path("", include(base_router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),
    path("signup/", UserViewset.as_view({"post": "create"}), name="signup"),
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
