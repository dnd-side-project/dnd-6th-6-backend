from rest_framework.permissions import BasePermission

class IsHouseMember(BasePermission):
    def has_permission(self, request, view):
        if not request.user.profile.house:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.profile.house != obj.assignee.profile.house:
            return False
        
        return True