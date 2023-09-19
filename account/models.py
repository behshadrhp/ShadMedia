from uuid import uuid4
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from utils import validator


class User(AbstractUser):
    '''This class is for defining the user model whose fields are included username and email'''

    # user information
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False, db_index=True)
    username = models.CharField(max_length=30, unique=True, validators=[validator.username_regex], blank=True, null=True)
    email = models.EmailField(unique=True, validators=[validator.email_regex])

    USERNAME_FIELD = 'username'  # & Password is required by default.

    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['-date_joined', '-is_superuser', '-is_staff', '-is_active',]
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
            models.Index(fields=['username',]),
            models.Index(fields=['email',]),
        ]

    def __str__(self):
        return self.username
        
    def validate_unique_email(self):
        '''
        Validates the uniqueness of the email.
        '''
        # Check if the email is already in use by other users
        existing_users = User.objects.filter(email=self.email)
        if self.pk:
            existing_users = existing_users.exclude(pk=self.pk)  # Exclude the current user from the check
        if existing_users.exists():
            raise ValidationError({'email': 'This email is already in use.'})

    def clean(self):
        '''
        Custom clean method to perform additional validation.
        '''
        if self.email:
            self.email = self.email.lower()  # Convert the email to lowercase
        self.validate_unique_email()  # Call the function to check email uniqueness    
        super().clean()
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.id:
            existing = Profile.objects.filter(id=self.id).first()
            if existing:
                if existing.avatar != self.avatar and 'img/' not in existing.avatar.name:
                    existing.avatar.delete(save=False)
            
        super().save(*args, **kwargs)
