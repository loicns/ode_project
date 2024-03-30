from django.db import models
from django.core.files.storage import default_storage
import hashlib  # for generating checksums

class StoredData(models.Model):
  filename = models.CharField(max_length=255)
  upload_date = models.DateTimeField(auto_now_add=True)
  file_size = models.IntegerField(null=True)  # Optional: can be set during upload
  content_type = models.CharField(max_length=255, null=True)  # Optional: can be set during upload
  checksum = models.CharField(max_length=255, unique=True)  # Unique identifier
  status = models.CharField(max_length=20, choices=[
      ('uploaded', 'Uploaded'),
      ('processing', 'Processing'),
      ('failed', 'Processing Failed'),
  ], default='uploaded')
  processing_details = models.TextField(blank=True)  # Optional processing logs
  source = models.CharField(max_length=255, blank=True)  # Optional source information

  def __str__(self):
    return f"{self.filename} ({self.upload_date})"

  def save(self, *args, **kwargs):
    # Generate checksum before saving
    if not self.checksum:
      with open(self.filepath, 'rb') as f:
        data = f.read()
        self.checksum = hashlib.sha256(data).hexdigest()
    super().save(*args, **kwargs)

  @property
  def filepath(self):
    return default_storage.path(self.filename)