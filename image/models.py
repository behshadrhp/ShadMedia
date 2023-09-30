from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

from utils.validator import character_regex

User = get_user_model()

class Image(models.Model):
    '''
    This class is for creating post images.
    '''

    # initial information
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True, validators=[character_regex])
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='image/%Y/%m/%d/')
    description = models.TextField(blank=True)
    users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)
    total_like = models.PositiveIntegerField(default=0)

    # create at & update at
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['-create_at']),
            models.Index(fields=['total_like'])
        ]
        ordering = ['-update_at', '-create_at']

    # Save the slug with the title input parameter
    def save(self, *args, **kwargs):
        if not self.slug or self.slug != self.title:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Image, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('image:image_detail', kwargs={'pk': self.pk, 'slug': self.slug})
    
    def __str__(self):
        return self.title
