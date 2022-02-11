from rest_framework.permissions import BasePermission

class IsHouseMember(BasePermission):
    def has_permission(self, request, view):
        if not request.user.user_profile.house:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.user_profile.house != obj.assignee.user_profile.house:
            return False
        
        return True