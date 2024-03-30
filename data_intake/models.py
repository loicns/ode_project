from django.db import models

# This model stores information about uploaded files.
from django.db import models

class Upload(models.Model):
    source = models.CharField(max_length=255)  # Upload source (e.g., drag-and-drop, form)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of upload
    file = models.FileField(upload_to='uploads/', null=True, default='defaultvalue')  # Adjust upload path if needed
    data = models.CharField(max_length=100, null=True, default='defaultvalue')

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at})"