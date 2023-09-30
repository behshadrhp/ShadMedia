from django.contrib import admin
from django.http import HttpRequest

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    '''
    UserAdmin class is for creating and displaying users and can be managed from this section.
    ''' 

    list_display = ('username', 'email', 'is_active', 'is_staff', 'last_login', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'last_login')
    search_fields = ['username__icontains', 'email__icontains']
    fields = [
        'username', 
        'email',
        'is_active',
        'is_staff', 
        'is_superuser',
        'groups',
        'user_permissions',
        'last_login', 
        'date_joined'
        ]
    ordering = ['-is_superuser', '-is_staff', '-is_active', '-last_login']
    list_per_page = 10

    def has_add_permission(self, request: HttpRequest):
          return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None):
          return True

    def has_change_permission(self, request: HttpRequest, obj=None):
        if request.user.is_superuser and obj is not None and not obj.is_superuser:
            return True
        elif obj is not None and request.user.is_authenticated: # Checks whether the user is authenticated or not empty.
            if obj.username == request.user.username:
                return True
            elif obj.username is None and obj == request.user.username: # Checks if the user is the same person.
                return True
            else:
                return False
        else:
            False


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['owner', 'first_name', 'last_name', 'birthday']
    fields = ['avatar', 'first_name', 'last_name', 'birthday']
    list_per_page = 10
    search_fields = ['first_name__icontains', 'last_name__icontains', 'email__icontains']
    readonly_fields = ['owner']

    def has_add_permission(self, request: HttpRequest):
          return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None):
          return True

    def has_change_permission(self, request: HttpRequest, obj=None):

        if obj is not None and request.user.is_authenticated: # Checks whether the user is authenticated or not empty.
            if obj.owner.username == request.user.username:
                return True
            elif obj.owner.username is None and obj == request.user.username: # Checks if the user is the same person.
                return True
            else:
                return False
        return super().has_change_permission(request, obj)
