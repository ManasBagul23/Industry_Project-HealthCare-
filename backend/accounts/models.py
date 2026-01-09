from django.db import models

from django.contrib.auth.models import User




class UserProfile(models.Model):
    LIFE_STAGE_CHOICES = [
        ('adult', 'Adult'),
        ('pregnant', 'Pregnant'),
        ('lactating', 'Lactating'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    life_stage = models.CharField(max_length=20, choices=LIFE_STAGE_CHOICES)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    diet_type = models.CharField(max_length=50)


class DietitianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username