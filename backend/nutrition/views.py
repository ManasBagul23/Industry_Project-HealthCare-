from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import FoodItem, FoodLog
from .serializers import FoodItemSerializer, FoodLogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from .ai_langchain import generate_explainable_advice
from .ml_features import extract_user_features
from .ml_predict import predict_risk
from .exercise_rules import get_exercise_plan
from .ai_exercise import explain_exercise
from .regions import STATE_TO_REGION
from .regional_foods import REGIONAL_FOODS



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