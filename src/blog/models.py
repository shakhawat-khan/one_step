from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 
from django.utils import timezone
from causes.models import Catagory
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    thumbnail = models.ImageField(blank=True, upload_to='blog_pics')
    catagory = models.ManyToManyField(Catagory)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def total_likes(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))