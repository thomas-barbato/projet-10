from django.contrib.auth.backends import ModelBackend
from ..models import Users


class EmailModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(email__iexact=username)
        except Users.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
