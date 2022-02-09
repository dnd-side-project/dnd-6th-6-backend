from django.db import models
from django.contrib.auth.models import User

# Create your models here.


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
        ("INTJ", "INTJ"),
        ("​INTP", "​INTP"),
        ("ENTJ", "ENTJ"),
        ("ENTP", "ENTP"),
        ("INFJ", "INFJ"),
        ("INFP", "INFP"),
        ("ENFJ", "ENFJ"),
        ("ENFP", "ENFP"),
        ("ISTJ", "ISTJ"),
        ("ISFJ", "ISFJ"),
        ("ESTJ", "ESTJ"),
        ("ESFJ", "ESFJ"),
        ("ISTP", "ISTP"),
        ("ISFP", "ISFP"),
        ("ESTP", "ESTP"),
        ("ESFP", "ESFP"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    house = models.ForeignKey(
        "houses.House",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile",
    )

    gender = models.CharField(choices=GENDER_CHOICES, blank=False, max_length=10)
    # avatar = models.ImageField(blank=True)
    life_pattern = models.CharField(choices=LIFE_CHOICES, blank=True, max_length=10)
    disposition = models.CharField(
        choices=DISPOSITION_CHOICE, blank=True, max_length=10
    )
    mbti = models.CharField(choices=MBTI_CHOICE, blank=True, max_length=5)
    message = models.TextField(blank=True, max_length=30)

    def __str__(self):
        return self.user.first_name
