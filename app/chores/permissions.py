from rest_framework.permissions import BasePermission

class IsHouseMember(BasePermission):
    def has_permission(self, request, view):
        profile = request.user.user_profile
        return bool(
            profile and
            profile.house and
            profile.house.id == int(view.kwargs["house_id"])
        )