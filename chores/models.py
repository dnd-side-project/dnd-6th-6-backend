from django.contrib.auth.models import User
from django.db import models

from houses.models import House

class Category(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class ChoreInfo(models.Model):
    name = models.CharField(max_length=255)
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default=1
    )

    def __str__(self):
        return self.name


class Chore(models.Model):
    assignees = models.ManyToManyField(
        User,
        related_name="chores",
        related_query_name="has_chore"
    )
    information = models.ForeignKey(
        ChoreInfo,
        on_delete=models.CASCADE,
        related_name="chores",
        related_query_name="chore"
    )
    planned_at = models.DateTimeField()
    completed_at = models.DateTimeField(
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.assignees}'s {self.information}"
    
    class Meta:
        ordering = ["-planned_at"]


class Day(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class RepeatChore(models.Model):

    class allocation_method(models.IntegerChoices):
        FIX = 1
        ORDER = 2
        RANDOM = 3

    information = models.OneToOneField(
        ChoreInfo,
        on_delete=models.CASCADE
    )
    assignees = models.ManyToManyField(
        User,
        related_name="repeat_chores",
        related_query_name="has_repeat_chores"
    )
    allotcaion_method = models.PositiveSmallIntegerField(
        allocation_method
    )
    days = models.ManyToManyField(Day)