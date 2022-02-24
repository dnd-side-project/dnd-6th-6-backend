from django.shortcuts import get_object_or_404

from rest_framework.permissions import BasePermission

from chores.models import Chore, RepeatChore

class IsHouseMember(BasePermission):
    def has_permission(self, request, view):
        profile = request.user.user_profile
        chore_id = view.kwargs.get("chore_id")
        repeat_chore_id = view.kwargs.get("repeat_chore_id")
        if chore_id:
            chore = get_object_or_404(Chore, pk=int(chore_id))
        elif repeat_chore_id:
            chore = get_object_or_404(RepeatChore, pk=int(repeat_chore_id))
        
        return bool(
            profile and
            profile.house and
            profile.house == chore.information.house
        )
        