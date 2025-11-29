from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.name

class Room(models.Model):
    CATEGORY_CHOICES = [
        ("single","싱글"),("double","더블"),("twin","트윈"),
        ("family","패밀리"),("suite","스위트"),
    ]
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    capacity = models.PositiveIntegerField(default=1)
    price_per_night = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self): return f"{self.number} - {self.name}"
