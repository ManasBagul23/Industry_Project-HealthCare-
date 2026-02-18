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


# ============================================
# Nutrition Deficiency Assessment Serializers
# ============================================

class QuestionnaireResponsesSerializer(serializers.Serializer):
    """Serializer for questionnaire responses"""
    fatigue = serializers.CharField(required=False, allow_blank=True, default="")
    hair_fall = serializers.CharField(required=False, allow_blank=True, default="")
    muscle_cramps = serializers.CharField(required=False, allow_blank=True, default="")
    sun_exposure_minutes_per_day = serializers.CharField(required=False, allow_blank=True, default="30")
    dairy_servings_per_day = serializers.CharField(required=False, allow_blank=True, default="1")
    green_leafy_frequency_per_week = serializers.CharField(required=False, allow_blank=True, default="3")
    water_source = serializers.CharField(required=False, allow_blank=True, default="")


class NutritionAssessmentInputSerializer(serializers.Serializer):
    """Input serializer for nutrition deficiency assessment"""
    age = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    height_cm = serializers.CharField(required=True)
    weight_kg = serializers.CharField(required=True)
    health_category = serializers.CharField(required=False, allow_blank=True, default="adult")
    dietary_preference = serializers.CharField(required=False, allow_blank=True, default="vegetarian")
    location = serializers.CharField(required=False, allow_blank=True, default="")
    morning_habits = serializers.CharField(required=False, allow_blank=True, default="")
    afternoon_habits = serializers.CharField(required=False, allow_blank=True, default="")
    evening_habits = serializers.CharField(required=False, allow_blank=True, default="")
    questionnaire_responses = QuestionnaireResponsesSerializer(required=False)
    
    def validate_age(self, value):
        """Validate age is a positive number"""
        try:
            age = float(value.replace(",", "").strip()) if isinstance(value, str) else float(value)
            if age <= 0 or age > 120:
                raise serializers.ValidationError("Age must be between 1 and 120")
            return value
        except (ValueError, AttributeError):
            raise serializers.ValidationError("Age must be a valid number")
    
    def validate_height_cm(self, value):
        """Validate height is reasonable"""
        try:
            height = float(value.replace(",", "").strip()) if isinstance(value, str) else float(value)
            if height <= 0 or height > 300:
                raise serializers.ValidationError("Height must be between 1 and 300 cm")
            return value
        except (ValueError, AttributeError):
            raise serializers.ValidationError("Height must be a valid number")
    
    def validate_weight_kg(self, value):
        """Validate weight is reasonable"""
        try:
            weight = float(value.replace(",", "").strip()) if isinstance(value, str) else float(value)
            if weight <= 0 or weight > 500:
                raise serializers.ValidationError("Weight must be between 1 and 500 kg")
            return value
        except (ValueError, AttributeError):
            raise serializers.ValidationError("Weight must be a valid number")
    
    def validate_gender(self, value):
        """Validate gender"""
        if value.lower() not in ["male", "female", "other"]:
            raise serializers.ValidationError("Gender must be male, female, or other")
        return value


class BMIAnalysisSerializer(serializers.Serializer):
    """Serializer for BMI analysis output"""
    bmi_value = serializers.FloatField()
    category = serializers.CharField()
    interpretation = serializers.CharField()


class DeficiencyRiskSerializer(serializers.Serializer):
    """Serializer for individual nutrient deficiency risk"""
    nutrient = serializers.CharField()
    risk_level = serializers.CharField()
    probability_percent = serializers.FloatField()
    recommended_intake = serializers.CharField()
    estimated_intake = serializers.CharField()
    coverage_percent = serializers.FloatField()
    primary_causes = serializers.ListField(child=serializers.CharField())
    symptom_links = serializers.ListField(child=serializers.CharField())
    geographic_influence = serializers.CharField()


class AlertSerializer(serializers.Serializer):
    """Serializer for alerts"""
    type = serializers.CharField()
    nutrient = serializers.CharField()
    message = serializers.CharField()
    action = serializers.CharField()
    priority = serializers.IntegerField()


class DietaryRecommendationSerializer(serializers.Serializer):
    """Serializer for dietary recommendations"""
    category = serializers.CharField()
    nutrient = serializers.CharField(required=False, allow_blank=True)
    priority = serializers.CharField()
    foods = serializers.ListField(child=serializers.CharField(), required=False)
    tip = serializers.CharField(required=False, allow_blank=True)
    action = serializers.CharField(required=False, allow_blank=True)
    tests = serializers.ListField(child=serializers.CharField(), required=False)


class NutrientComparisonSerializer(serializers.Serializer):
    """Serializer for nutrient comparison chart data"""
    nutrient = serializers.CharField()
    who_rda = serializers.FloatField()
    estimated_intake = serializers.FloatField()
    coverage_percent = serializers.FloatField()


class RiskRadarSerializer(serializers.Serializer):
    """Serializer for risk radar chart data"""
    nutrient = serializers.CharField()
    risk_probability = serializers.FloatField()
    risk_level = serializers.CharField()


class VisualizationDataSerializer(serializers.Serializer):
    """Serializer for visualization data"""
    nutrient_comparison_chart = NutrientComparisonSerializer(many=True)
    risk_radar_chart = RiskRadarSerializer(many=True)
    heatmap_region_flag = serializers.CharField()
    urban_trend_flag = serializers.CharField()


class NutritionAssessmentOutputSerializer(serializers.Serializer):
    """Output serializer for complete nutrition deficiency assessment"""
    bmi_analysis = BMIAnalysisSerializer()
    demographic_summary = serializers.CharField()
    deficiency_risks = DeficiencyRiskSerializer(many=True)
    alerts = AlertSerializer(many=True)
    recommendations = DietaryRecommendationSerializer(many=True)
    visualization_data = VisualizationDataSerializer()

