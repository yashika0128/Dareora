
from django.db import models
from django.contrib.auth.models import User
import uuid

# Model to store dare completions
class DareCompletion(models.Model):
    dare = models.ForeignKey('postdare.Dare_project', on_delete=models.CASCADE, related_name='completions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dare_completions')
    completion_notes = models.TextField()
    proof_file = models.FileField(upload_to='dare_proofs/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} completed {self.dare.dare_title}"

# Private Room for group dares
class PrivateRoom(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    members = models.ManyToManyField(User, related_name='private_rooms')
    created_by = models.ForeignKey(User, related_name='created_rooms', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Dares posted in a private room
class PrivateRoomDare(models.Model):
    room = models.ForeignKey(PrivateRoom, related_name='dares', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name='private_room_dares', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
