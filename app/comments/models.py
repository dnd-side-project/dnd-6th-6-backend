from django.db import models

from chores.models import Chore, RepeatChore
from users.models import User

class CommentChore(models.Model):
    writer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments_chore",
        related_query_name="comment_chore"
    )
    chore = models.ForeignKey(
        Chore,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment"
    )
    content = models.CharField(max_length=255)
    writed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["writed_at"]

class CommentRepeatChore(models.Model):
    writer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments_repeat_chore",
        related_query_name="comment_repeat_chore"
    )
    repeat_chore = models.ForeignKey(
        RepeatChore,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment"
    )
    content = models.CharField(max_length=255)
    writed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["writed_at"]