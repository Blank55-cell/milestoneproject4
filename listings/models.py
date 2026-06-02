from django.db import models

# Create your models here.
from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price = models.IntegerField()  # Stored as a whole number (e.g., 450000)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    is_featured = models.BooleanField(default=False) # Useful for filtering home page items later
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Properties"