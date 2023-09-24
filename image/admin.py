from django.contrib import admin
from image.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    '''
    image admin panel.
    '''

    list_display = ['owner', 'title', 'create_at']
    list_filter = ['owner', 'update_at']
    search_fields = ['title__icontains', 'description__icontains']
    prepopulated_fields = {
        'slug': ('title',)
    }
    fields = ['image', 'title', 'slug', 'url', 'description', 'users_like']
    readonly_fields = ['owner']

     # save owner
    def save_model(self, request, obj, form, change):
            # change owner field to owner requested
            obj.owner = request.user
            return super().save_model(request, obj, form, change)
