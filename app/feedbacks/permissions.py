from django.shortcuts import get_object_or_404

from rest_framework.permissions import BasePermission

from chores.models import Chore

class IsHouseMember(BasePermission):
    def has_permission(self, request, view):
        profile = request.user.user_profile
        chore_id = int(view.kwargs["chore_id"])
        chore = get_object_or_404(Chore, pk=chore_id)
        return bool(
            profile and
            profile.house and
            profile.house == chore.information.house
        )
    
    def has_object_permission(self, request, view, obj):
        return bool(obj._from == request.user)