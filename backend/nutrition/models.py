from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    iron = models.FloatField()
    calcium = models.FloatField()
    protein = models.FloatField()
    region = models.CharField(max_length=100)

class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date = models.DateField(auto_now_add=True)
