from enum import unique
from django.core.checks import messages
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.conf import settings

import misaka

from groups.models import Group
# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(
        Group, related_name='posts', null=True, blank=True, on_delete=CASCADE)

    def __str__(self) -> str:
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("posts:single", kwargs={"username": self.user.username,'pk':self.pk})
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']
        
