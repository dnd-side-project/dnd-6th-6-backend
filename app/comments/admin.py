from django.contrib import admin

from comments.models import CommentChore, CommentRepeatChore

admin.site.register(CommentChore)
admin.site.register(CommentRepeatChore)