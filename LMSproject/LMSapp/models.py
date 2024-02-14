from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User



class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_location = models.CharField(max_length=255, blank=True, null=True)
    doc_location = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return (self.user)
    


