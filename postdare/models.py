from django.db import models
from django.contrib.auth.models import User

class Dare_project(models.Model):
    # User field add kar rahe hain
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dares')
    
    # Existing fields
    dare_title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    time_limit = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=10, default='Moderate')
    tags = models.CharField(max_length=200, blank=True, null=True)
    
    # Additional helpful fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.dare_title} by {self.user.username}"