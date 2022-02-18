from rest_framework.permissions import BasePermission

class IsHouseMember(BasePermission):
    def has_permission(self, request, view):
        profile = request.user.user_profile
        requested_house_id = int(view.kwargs["house_id"])
        return bool(
            profile and
            profile.house and
            profile.house.id == requested_house_id
        )
    
    def has_object_permission(self, request, view, obj):
        requested_house_id = int(view.kwargs["house_id"])
        return bool(obj.information.house.id == requested_house_id)