import datetime
import random

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from chores.models import RepeatChore, Chore

def get_assignees_by_random(assignees):
    return [random.choice(assignees)]

def add_chore(instance, action, **kwargs):
    if action=="post_add":
        repeat_chore = instance
        information = repeat_chore.information
        days = repeat_chore.days.all()
        today = datetime.datetime.today()
        today_week = today.weekday() + 1
        
        for day in days:
            if today_week>day.id:
                continue
            days_delta = day.id - today_week
            planned_at = repeat_chore.planned_at
            next_planned_at = datetime.datetime(
                today.year,
                today.month,
                today.day,
                planned_at.hour,
                planned_at.minute,
                planned_at.second
            ) + datetime.timedelta(days=days_delta)
            
            method = repeat_chore.allocation_method
            choices = RepeatChore.AllocationMethod
            assignees = list(repeat_chore.assignees.all())
            
            if method == choices.FIX:
                next_assignees = assignees
            elif method == choices.ORDER:
                if information.chores.all().exists():
                    last_chore = information.chores.last()
                    last_chore_assignees = last_chore.assignees.all()
                    for i, assignee in enumerate(assignees):
                        if assignee==last_chore_assignees.first():
                            if i+1==len(assignees):
                                next_assignees = [assignees[0]]
                            else:
                                next_assignees = [assignees[i+1]]
                            break
                else:
                    next_assignees = [assignees[0]]

            elif method == choices.RANDOM:
                next_assignees = get_assignees_by_random(assignees)
        
            chore = Chore.objects.create(
                information=information,
                planned_at=next_planned_at
            )
            chore.assignees.set(next_assignees)

m2m_changed.connect(
    add_chore,
    sender=RepeatChore.days.through
)