from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile", null=False
    )
    house = models.ForeignKey(
        "houses.House",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile",
    )
    avatar = models.ImageField(upload_to="users/images/%Y/%m/%d", blank=True)

    def __str__(self):
        return f"{self.user}"


# test
class SocialUser(models.Model):
    username = models.EmailField()
    first_name = models.CharField(max_length=20, null=True)
    provider = models.CharField(max_length=6)  # kakao/naver
    profile = models.OneToOneField("Profile", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username} || {self.provider}"


class EmailAuth(models.Model):
    signup_email = models.EmailField(null=True)
    code = models.CharField(null=True, max_length=6)
    using = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} :: {self.using}"
