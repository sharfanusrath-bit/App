from django.db import models
from django.contrib.auth.models import User

class Evidence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)
    file = models.FileField(upload_to='evidence_files/')
    file_hash = models.CharField(max_length=64)
    blockchain_tx = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidence #{self.id} - {self.user.username}"
