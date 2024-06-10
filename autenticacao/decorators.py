from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def group_required(group_name, login_url=None):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(login_url or 'login')  # Use the provided login_url or default to 'login'
            if not request.user.groups.filter(name=group_name).exists():
                raise PermissionDenied  # Raise an exception if the user is not in the group
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
