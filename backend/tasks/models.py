from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Task(models.Model):
    NOT_STARTED_STATUS = "N"
    IN_PROGRESS_STATUS = "I"
    DONE_STATUS = "D"
    STATUS_CHOICES = [
        (NOT_STARTED_STATUS, "Not Started"),
        (IN_PROGRESS_STATUS, "In Progress"),
        (DONE_STATUS, "Done"),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=NOT_STARTED_STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.status}) by {self.user.username}"
    
    def validate_title(value):
        if len(value.strip()) < 3:
            raise ValidationError("Title must be at least 3 characters long")
        if not value.isalnum():
            raise ValidationError("Title must be alphanumeric")
        
    def clean(self):
        original_record = Task.objects.get(self.pk)
        if original_record.status == self.DONE_STATUS:
            raise ValidationError("Cannot update a task that is already done")

        if (self.status is self.DONE_STATUS) and (original_record.status is self.NOT_STARTED_STATUS):
            raise ValidationError("Status is not allowed to update to 'Done' status")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.title = self.title.strip().lower()
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "title"])
        ]