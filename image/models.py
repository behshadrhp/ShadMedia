from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()

class Image(models.Model):
    '''
    Image post.
    '''

    # initial information
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m/%d/')
    description = models.TextField(blank=True)
    users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)

    # create at & update at
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['-create_at'])
        ]
        ordering = ['-update_at', '-create_at']

    # Save the slug with the title input parameter
    def save(self, *args, **kwargs):
        if not self.slug or self.slug != self.title:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Image, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
