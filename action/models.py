from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()


class Action(models.Model):
    '''
    This class is for review users actions and activities.
    '''

    # initial information
    owner = models.ForeignKey(User, related_name='action', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)

    # ContentType Model 
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    # create at
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-create_at']),
            models.Index(fields=['target_ct', 'target_id']),
        ]
        ordering = ['-create_at']
