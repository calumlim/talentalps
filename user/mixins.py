from django.contrib.auth.mixins import AccessMixin

class StaffAccessMixin(AccessMixin):
    if not (request.user.is_authenticated and request.user.is_staff):
        return self.handle_no_permission()
    return super().dispatch(request, *args, **kwargs)

class EmployerAccessMixin(AccessMixin):
    if not (request.user.is_authenticated and request.user.userprofile.is_employer):
        return self.handle_no_permission()
    return super().dispatch(request, *args, **kwargs)