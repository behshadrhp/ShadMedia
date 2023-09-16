from django.contrib import admin
from django.http import HttpRequest

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['owner', 'first_name', 'last_name', 'birthday']
    fields = ['avatar', 'first_name', 'last_name', 'birthday']
    list_per_page = 10
    search_fields = ['first_name__icontains', 'last_name__icontains', 'email__icontains']
    readonly_fields = ['owner']

    def has_add_permission(self, request: HttpRequest):
          return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None):
          return False

    def has_change_permission(self, request: HttpRequest, obj=None):

        if obj is not None and request.user.is_authenticated: # Checks whether the user is authenticated or not empty.
            if obj.owner.username == request.user.username:
                return True
            elif obj.owner.username is None and obj == request.user.username: # Checks if the user is the same person.
                return True
            else:
                return False
        return super().has_change_permission(request, obj)
