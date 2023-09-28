from django.contrib import admin

from . import models


@admin.register(models.Action)
class ActionAdmin(admin.ModelAdmin):
    '''
    This class is for managing and reviews action model on admin panel.
    '''

    list_display = ['owner', 'verb', 'target', 'create_at']
    list_filter = ['owner', 'create_at']    
    search_fields = ['verb__icontains']
    