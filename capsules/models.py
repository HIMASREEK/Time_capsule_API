from django.db import models
from django.contrib.auth.models import User
import uuid

class Capsule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    unlock_date = models.DateTimeField()
    image = models.ImageField(upload_to='capsules/', null=True, blank=True)

    is_opened = models.BooleanField(default=False)

    # 🔗 Share Token
    share_token = models.UUIDField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.share_token:
            self.share_token = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title