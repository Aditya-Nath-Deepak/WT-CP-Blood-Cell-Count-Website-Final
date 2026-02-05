from django.db import models

# Create your models here.
class DetectionCountModel(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Total Detections: {self.count}"