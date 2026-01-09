from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FoodItemViewSet,
    FoodLogViewSet,
    DailyNutritionSummary,
    DeficiencyStatus,
    GeoFoodRecommendation,
    WeeklySummary,
    NutritionRiskPrediction,
    ExerciseRecommendation,
)

router = DefaultRouter()
router.register('food-items', FoodItemViewSet)
router.register('food-logs', FoodLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', DailyNutritionSummary.as_view()),
    path('deficiency/', DeficiencyStatus.as_view()),
    path('recommendations/', GeoFoodRecommendation.as_view()),
    path('weekly/', WeeklySummary.as_view()),
    path("risk/", NutritionRiskPrediction.as_view()),
    path("exercise/", ExerciseRecommendation.as_view()),
]
