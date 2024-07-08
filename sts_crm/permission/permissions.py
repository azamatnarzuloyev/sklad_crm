from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    message = "You Must Be SuperUser"

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_superuser)


class IsSuperUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user.is_authenticated and request.user.is_superuser)


class IsSuperUserOrAuthor(BasePermission):
    message = "You Must Be SuperUser or Author"

    def has_permission(self, request, view):
        print(request)
        return bool(
            request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_authenticated
            and request.user.author
        )


class IsSuperUserOrAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_authenticated
            and obj.author == request.user
        )


class DokonUserAuthentication(BasePermission):
    message = "data not fount"

    def has_permission(self, request, obj):
        return bool(
            request.user.is_authenticated
            and request.user.vendor_user
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        if request.user.vendor_user:
            return True
        else:
            return False


class DokonUserSHopAuthentication(BasePermission):
    message = "data not fount"

    def has_permission(self, request, obj):
        return bool(request.user.is_authenticated and request.user.vendor_user)
