import datetime
import random

from chores.models import RepeatChore, Chore
from users.models import User

def get_assignees_by_random(assignees):
    return [random.choice(assignees)]

def add_chore_auto():
    repeat_chores = RepeatChore.objects.all()
    for repeat_chore in repeat_chores:
        information = repeat_chore.information
        days = repeat_chore.days.all()
        today = datetime.datetime.today()
        today_week = today.weekday() + 1

        for day in days:
            if today_week>=day.id:
                day.id += 7
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
                last_chore = information.chores.last()
                last_chore_assignees = last_chore.assignees.all()
                if len(last_chore_assignees)>1:
                    next_assignees = get_assignees_by_random(assignees)
                else:
                    members = list(User.objects.filter(
                        user_profile__house=information.house
                    ))
                    for i, assignee in enumerate(assignees):
                        if assignee==last_chore_assignees.first():
                            if i+1==len(assignees):
                                next_assignees = [assignees[0]]
                            else:
                                next_assignees = [assignees[i+1]]
                            break
            elif method == choices.RANDOM:
                next_assignees = get_assignees_by_random(assignees)
        
            chore = Chore.objects.create(
                information=information,
                planned_at=next_planned_at
            )
            chore.assignees.set(next_assignees)