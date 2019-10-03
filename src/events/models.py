from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    about = models.TextField()
    thumbnail = models.ImageField(blank=True, upload_to='events_pics')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='personWroted')
    area = models.CharField(max_length=30)
    date_posted = models.DateTimeField(default=timezone.now)
    eventTime = models.DateField()
    joined = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title