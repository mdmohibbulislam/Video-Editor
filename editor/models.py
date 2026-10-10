from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    original_file = models.FileField(upload_to='videos/originals/')
    processed_file = models.FileField(upload_to='videos/processed/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title