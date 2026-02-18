from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import FoodItem, FoodLog
from .serializers import (
    FoodItemSerializer, 
    FoodLogSerializer,
    NutritionAssessmentInputSerializer,
    NutritionAssessmentOutputSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .ai_langchain import generate_explainable_advice
from .ml_features import extract_user_features
from .ml_predict import predict_risk
from .exercise_rules import get_exercise_plan
from .ai_exercise import explain_exercise
from .regions import STATE_TO_REGION
from .regional_foods import REGIONAL_FOODS
from .deficiency_engine import assess_nutrition_deficiency



RDA_MAP = {
    "adult": {
        "iron": 18,
        "calcium": 1000,
        "protein": 46
    },
    "pregnant": {
        "iron": 27,
        "calcium": 1000,
        "protein": 71
    },
    "lactating": {
        "iron": 9,
        "calcium": 1300,
        "protein": 71
    }
}



class FoodItemViewSet(ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]

class FoodLogViewSet(ModelViewSet):
    queryset = FoodLog.objects.all()
    serializer_class = FoodLogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DailyNutritionSummary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        logs = FoodLog.objects.filter(user=request.user, date=today)

        iron = 0
        calcium = 0
        protein = 0

        for log in logs:
            factor = log.quantity / 100
            iron += log.food.iron * factor
            calcium += log.food.calcium * factor
            protein += log.food.protein * factor

        return Response({
            "date": today,
            "iron": round(iron, 2),
            "calcium": round(calcium, 2),
            "protein": round(protein, 2)
        })

class DeficiencyStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        life_stage = profile.life_stage

        rda = RDA_MAP.get(life_stage, RDA_MAP["adult"])

        today = date.today()
        logs = FoodLog.objects.filter(user=request.user, date=today)

        totals = {
            "iron": 0.0,
            "calcium": 0.0,
            "protein": 0.0
        }

        for log in logs:
            factor = log.quantity / 100
            totals["iron"] += log.food.iron * factor
            totals["calcium"] += log.food.calcium * factor
            totals["protein"] += log.food.protein * factor

        status = {}
        for nutrient in totals:
            if totals[nutrient] < 0.8 * rda[nutrient]:
                status[nutrient] = "LOW"
            elif totals[nutrient] > 1.2 * rda[nutrient]:
                status[nutrient] = "HIGH"
            else:
                status[nutrient] = "ADEQUATE"

        # 📍 Region logic
        state = profile.state
        region = STATE_TO_REGION.get(state, "West India")

        regional_suggestions = {}
        for nutrient, level in status.items():
            if level == "LOW":
                regional_suggestions[nutrient] = REGIONAL_FOODS.get(region, {}).get(nutrient, [])

        # 🤖 LangChain nutrition explanation (CORRECT)
        try:
            ai_explanation = generate_explainable_advice(
                life_stage=life_stage,
                status=status,
                region=region
            )
        except Exception:
            ai_explanation = "AI explanation unavailable."

        return Response({
            "life_stage": life_stage,
            "region": region,
            "intake": {
                "iron": round(totals["iron"], 2),
                "calcium": round(totals["calcium"], 2),
                "protein": round(totals["protein"], 2)
            },
            "status": status,
            "regional_food_suggestions": regional_suggestions,
            "ai_explanation": ai_explanation,
            "disclaimer": "This is not medical advice."
        })




class GeoFoodRecommendation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        state = profile.state

        deficient = []
        today = date.today()
        logs = FoodLog.objects.filter(user=request.user, date=today)

        iron = calcium = protein = 0
        for log in logs:
            factor = log.quantity / 100
            iron += log.food.iron * factor
            calcium += log.food.calcium * factor
            protein += log.food.protein * factor

        if iron < 0.8 * RDA["iron"]:
            deficient.append("iron")
        if calcium < 0.8 * RDA["calcium"]:
            deficient.append("calcium")
        if protein < 0.8 * RDA["protein"]:
            deficient.append("protein")

        foods = FoodItem.objects.filter(region=state)

        recommendations = {}
        for nutrient in deficient:
            recommendations[nutrient] = [
                food.name for food in foods if getattr(food, nutrient) > 0
            ][:5]

        return Response({
            "state": state,
            "recommendations": recommendations
        })


class WeeklySummary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        week_data = []

        for i in range(7):
            day = today - timedelta(days=i)
            logs = FoodLog.objects.filter(user=request.user, date=day)

            iron = calcium = protein = 0
            for log in logs:
                factor = log.quantity / 100
                iron += log.food.iron * factor
                calcium += log.food.calcium * factor
                protein += log.food.protein * factor

            week_data.append({
                "date": day,
                "iron": round(iron, 2),
                "calcium": round(calcium, 2),
                "protein": round(protein, 2)
            })

        return Response(week_data[::-1])


class NutritionRiskPrediction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        features = extract_user_features(request.user)

        if not features:
            return Response(
                {"message": "Not enough data for ML risk prediction"},
                status=400
            )

        prediction = predict_risk(features)

        return Response({
            "features": features,
            "prediction": prediction
        })
class ExerciseRecommendation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        features = extract_user_features(request.user)

        if not features:
            return Response(
                {"message": "Not enough data for exercise recommendation"},
                status=400
            )

        prediction = predict_risk(features)
        plan = get_exercise_plan(
            life_stage=profile.life_stage,
            risk_level=prediction["risk_level"]
        )

        return Response({
            "life_stage": profile.life_stage,
            "risk_level": prediction["risk_level"],
            "confidence": prediction["confidence"],
            "exercise_plan": plan,
            "disclaimer": "Exercise suggestions are general and not a substitute for professional advice."
        })

class ExerciseRecommendation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        features = extract_user_features(request.user)

        if not features:
            return Response(
                {"message": "Not enough data for exercise recommendation"},
                status=400
            )

        prediction = predict_risk(features)

        plan = get_exercise_plan(
            life_stage=profile.life_stage,
            risk_level=prediction["risk_level"]
        )

        # 🔹 LangChain explanation (safe + optional)
        try:
            ai_explanation = explain_exercise(
                life_stage=profile.life_stage,
                risk_level=prediction["risk_level"],
                exercise_plan=plan
            )
        except Exception as e:
            ai_explanation = "AI explanation unavailable."

        return Response({
            "life_stage": profile.life_stage,
            "risk_level": prediction["risk_level"],
            "confidence": prediction["confidence"],
            "exercise_plan": plan,
            "ai_explanation": ai_explanation,
            "disclaimer": "Exercise suggestions are general and not a substitute for professional advice."
        })


class NutritionDeficiencyAssessment(APIView):
    """
    AI-Powered Personalized Nutrition & Deficiency Risk Assessment Engine
    
    Analyzes user demographic, lifestyle, dietary, and geographic inputs
    to estimate potential nutrient deficiencies and generate structured
    JSON output for dashboard visualization.
    
    POST /nutrition/assessment/
    """
    permission_classes = [AllowAny]  # Allow unauthenticated access for assessment
    
    def post(self, request):
        """
        Process nutrition deficiency assessment request
        
        Expected Input Format:
        {
            "age": "",
            "gender": "",
            "height_cm": "",
            "weight_kg": "",
            "health_category": "",
            "dietary_preference": "",
            "location": "",
            "morning_habits": "",
            "afternoon_habits": "",
            "evening_habits": "",
            "questionnaire_responses": {
                "fatigue": "",
                "hair_fall": "",
                "muscle_cramps": "",
                "sun_exposure_minutes_per_day": "",
                "dairy_servings_per_day": "",
                "green_leafy_frequency_per_week": "",
                "water_source": ""
            }
        }
        """
        # Validate input
        serializer = NutritionAssessmentInputSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Perform deficiency assessment
            user_data = serializer.validated_data
            assessment_result = assess_nutrition_deficiency(user_data)
            
            # Validate output structure
            output_serializer = NutritionAssessmentOutputSerializer(data=assessment_result)
            
            if output_serializer.is_valid():
                return Response(output_serializer.data)
            else:
                # Return raw result if serialization has issues
                return Response(assessment_result)
                
        except Exception as e:
            return Response(
                {"error": "Assessment failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        """
        GET endpoint for authenticated users - uses profile data
        """
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required for GET request. Use POST with user data for anonymous assessment."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            profile = request.user.userprofile
            
            # Build user data from profile
            user_data = {
                "age": str(profile.age),
                "gender": "female" if profile.life_stage in ["pregnant", "lactating"] else "female",  # Default
                "height_cm": str(profile.height),
                "weight_kg": str(profile.weight),
                "health_category": profile.life_stage,
                "dietary_preference": profile.diet_type,
                "location": profile.state,
                "morning_habits": "",
                "afternoon_habits": "",
                "evening_habits": "",
                "questionnaire_responses": {}
            }
            
            # Perform assessment
            assessment_result = assess_nutrition_deficiency(user_data)
            
            return Response(assessment_result)
            
        except Exception as e:
            return Response(
                {"error": "Assessment failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NutritionDeficiencyAssessmentAuth(APIView):
    """
    Authenticated version of the nutrition assessment that can combine
    profile data with additional questionnaire responses
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Process nutrition assessment with profile data supplemented by request data
        """
        try:
            profile = request.user.userprofile
            
            # Get questionnaire and habit data from request
            request_data = request.data
            
            # Build comprehensive user data
            user_data = {
                "age": str(profile.age),
                "gender": request_data.get("gender", "female"),
                "height_cm": str(profile.height),
                "weight_kg": str(profile.weight),
                "health_category": profile.life_stage,
                "dietary_preference": profile.diet_type,
                "location": profile.state,
                "morning_habits": request_data.get("morning_habits", ""),
                "afternoon_habits": request_data.get("afternoon_habits", ""),
                "evening_habits": request_data.get("evening_habits", ""),
                "questionnaire_responses": request_data.get("questionnaire_responses", {})
            }
            
            # Perform assessment
            assessment_result = assess_nutrition_deficiency(user_data)
            
            return Response(assessment_result)
            
        except AttributeError:
            return Response(
                {"error": "User profile not found. Please complete your profile first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Assessment failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )