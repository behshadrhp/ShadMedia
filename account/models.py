from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Profile(models.Model):
    '''This class is Profile set for acount.'''

    # information about
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='/img/profile_avatar.png', upload_to='profile/avatar/', blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(blank=True, null=True)

    # create at & update at
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update_at', '-create_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
