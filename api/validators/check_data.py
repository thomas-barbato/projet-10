"""import """
import re

from django.utils.safestring import mark_safe
from rest_framework import serializers

from ..models import Users


class CheckPasswordPolicy:
    """docstring"""

    def __init__(self):
        self.password_pattern = (
            "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        )

    def validate(self, password, password2):
        """
        Has minimum 8 characters in length
        At least one uppercase letter. You can remove this condition by removing (?=.*?[A-Z])
        At least one lowercase letter. You can remove this condition by removing (?=.*?[a-z])
        At least one digit. You can remove this condition by removing (?=.*?[0-9])
        At least one special character, You can remove this condition by removing (?=.*?[#?!@$%^&*-])
        """
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Les mots de passe saisis ne sont pas identiques"}
            )
        if re.match(self.password_pattern, password) is None:
            raise serializers.ValidationError(
                {
                    "password": (
                        "Votre mot de passe doit contenir à minima "
                        "8 caractères, "
                        "1 majuscule, "
                        "1 minuscule, "
                        "1 symbole, "
                        "1 chiffre "
                    )
                }
            )


class CheckUsernameAlreadyUsed:
    """docstring"""

    def __init__(self):
        self.table = Users

    def validate(self, user):
        """
        check if username already exists in db.
        """
        if self.table.objects.filter(username=user).exists() is True:
            raise serializers.ValidationError(
                {
                    "username": mark_safe(
                        '<div class="alert alert-danger text-center col-xl-12 col-md-12 col-sm-10 mt-1" role="alert">'
                        "<p><b><i class="
                        + '"fas fa-exclamation-triangle"'
                        + "></i> Votre nom doit être unique.</b></p>"
                        "</div>"
                    )
                }
            )
