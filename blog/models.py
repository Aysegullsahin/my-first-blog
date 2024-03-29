from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

from .enums import PostStatus


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, blank=True)
    
    def __str__(self):
        return self.title
        
    def save(self, *arg, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*arg, **kwargs)        


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=50, blank=True)
    status = models.CharField(max_length=10, choices=PostStatus.AS_CHOICES)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def save(self, *arg, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*arg, **kwargs)    

    

