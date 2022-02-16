from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsHouseMember(BasePermission):
    def has_permission(self, request, view):
        profile = request.user.user_profile
        requested_house_id = int(view.kwargs["house_id"])
        return bool(
            profile and
            profile.house and
            profile.house.id == requested_house_id
        )

class IsWriterOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            obj.writer == request.user
        )