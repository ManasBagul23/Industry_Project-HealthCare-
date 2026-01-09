from django.contrib import admin

from .models import FoodItem, FoodLog

admin.site.register(FoodItem)
admin.site.register(FoodLog)

