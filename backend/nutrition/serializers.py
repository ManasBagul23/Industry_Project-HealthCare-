from rest_framework import serializers
from .models import FoodItem, FoodLog

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'
        

class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        fields = '__all__'
        read_only_fields = ['user']
