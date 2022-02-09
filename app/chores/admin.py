from django.contrib import admin

from chores.models import Category, ChoreInfo, Chore, Day, RepeatChore

admin.site.register(Category)
admin.site.register(ChoreInfo)
admin.site.register(Chore)
admin.site.register(Day)
admin.site.register(RepeatChore)