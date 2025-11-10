import os.path
from django.db import models
from django.utils import timezone

# Create your models here.
def uploads_to(instance, filename):
    created_at = timezone.now()
    return f"uploads/{created_at:%y%m%d}/{filename}"

class Upload(models.Model):
    file = models.FileField(upload_to=uploads_to)
    original_name = models.CharField(max_length=255, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)
    extension = models.CharField(max_length=20, blank=True)
    size_bytes = models.BigIntegerField(default=0)
    sha256 = models.CharField(max_length=64, blank=True)
    is_image = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name or os.path.basename(self.file.name)
