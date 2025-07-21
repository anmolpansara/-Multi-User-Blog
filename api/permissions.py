from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin'

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin can do anything
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin':
            return True
        
        # Editors can edit their own posts
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'editor':
            return obj.author == request.user
        
        return False

class CanCreatePost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return (request.user.is_authenticated and 
                   hasattr(request.user, 'userprofile') and 
                   request.user.userprofile.role in ['admin', 'editor'])
        return True

class CanViewPublishedOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins and editors can see all posts
        if (hasattr(request.user, 'userprofile') and 
            request.user.userprofile.role in ['admin', 'editor']):
            return True
        
        # Readers can only see published posts
        return obj.status == 'published'
