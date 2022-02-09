from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class ChoreInfo(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Chore(models.Model):
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
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
        return f"{self.assignee}'s {self.information}"

class RepeatChore(models.Model):
    information = models.OneToOneField(
        ChoreInfo,
        on_delete=models.CASCADE
    )
    assignees = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="repeat_chores",
        related_query_name="has_repeat_chores"
    )