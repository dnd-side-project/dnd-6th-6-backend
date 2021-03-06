from xml.parsers.expat import model
from django.db import models

from houses.models import House
from users.models import User

class Notice(models.Model):
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="notices",
        related_query_name="notice"
    )
    writer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notices",
        related_query_name="notice"
    )
    content = models.TextField()
    writed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ["-writed_at"]