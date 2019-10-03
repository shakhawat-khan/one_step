from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Catagory(models.Model):
    catagory = models.CharField(max_length=30)

    def __str__(self):
        return self.catagory


class Donation(models.Model):
    donatorID = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField()
    phone_number = models.CharField(max_length=14)
    donate_amount = models.IntegerField()
    
    def __str__(self):
        return f'{self.donatorID.username} Tk{self.donate_amount}'



class Cause(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(blank=True, upload_to='causes_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.IntegerField()
    raised = models.IntegerField(default=0)
    catagory = models.ManyToManyField(Catagory)
    area = models.CharField(max_length=30)
    division = models.CharField(blank=True,max_length=30)
    donation = models.ManyToManyField(Donation)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('cause-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title
    

