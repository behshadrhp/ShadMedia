import datetime

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from action.models import Action


def create_action(user, verb, target=None):
    '''
    This function is for create and apply user activity.
    '''

    # Check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_action = Action.objects.filter(owner_id=user.id, verb=verb, create_at__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_action = similar_action.filter(target_ct=target_ct, target_id=target.id)

    if not similar_action:
        # no existing actions found
        action = Action(owner=user, verb=verb, target=target)
        action.save()
        return True
    
    return False
