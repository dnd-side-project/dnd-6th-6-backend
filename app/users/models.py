from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here


class Profile(models.Model):
    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = (
        (GENDER_MALE, "남성"),
        (GENDER_FEMALE, "여성"),
    )

    LIFE_AM = "AM"
    LIFE_PM = "PM"
    LIFE_CHOICES = (
        (LIFE_AM, "아침형"),
        (LIFE_PM, "저녁형"),
    )

    DISPOSITION_COLLECTIVE = "collective"
    DISPOSITION_INDIVIDUQL = "individual"
    DISPOSITION_CHOICE = (
        (DISPOSITION_COLLECTIVE, "집단주의"),
        (DISPOSITION_INDIVIDUQL, "개인주의"),
    )

    MBTI_CHOICE = (
        ("intj", "INTJ"),
        ("intp", "​INTP"),
        ("entj", "ENTJ"),
        ("entp", "ENTP"),
        ("infj", "INFJ"),
        ("infp", "INFP"),
        ("emfj", "ENFJ"),
        ("enfp", "ENFP"),
        ("istj", "ISTJ"),
        ("isfj", "ISFJ"),
        ("estj", "ESTJ"),
        ("esfj", "ESFJ"),
        ("istp", "ISTP"),
        ("isfp", "ISFP"),
        ("estp", "ESTP"),
        ("esfp", "ESFP"),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile", null=True
    )
    house = models.ForeignKey(
        "houses.House",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile",
    )

    gender = models.CharField(choices=GENDER_CHOICES, blank=False, max_length=10)
    avatar = models.ImageField(upload_to="users/images/%Y/%m/%d", blank=True)
    life_pattern = models.CharField(choices=LIFE_CHOICES, blank=True, max_length=10)
    disposition = models.CharField(
        choices=DISPOSITION_CHOICE, blank=False, max_length=10
    )
    mbti = models.CharField(choices=MBTI_CHOICE, blank=True, max_length=5)
    message = models.TextField(blank=True, max_length=30)

    def __str__(self):
        return f"{self.user}"


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
