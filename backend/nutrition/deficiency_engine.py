"""
AI-Powered Personalized Nutrition & Deficiency Risk Assessment Engine
Main assessment module that performs comprehensive nutrient deficiency analysis
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .who_benchmarks import (
    calculate_bmi,
    get_rda_for_user,
    classify_risk_level,
    get_alert_type,
    WHO_RDA_BENCHMARKS
)
from .geographic_risk import (
    get_regional_anemia_data,
    get_groundwater_data,
    get_vitamin_d_regional_risk,
    get_dietary_risk_factors,
    get_symptom_correlations,
    get_recommended_test,
    SYMPTOM_NUTRIENT_CORRELATION,
    URBAN_DEFICIENCY_PATTERNS,
    DIETARY_RISK_FACTORS
)


class RiskLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class NutrientEstimate:
    """Estimated nutrient intake based on habits"""
    nutrient: str
    estimated_intake: float
    unit: str
    sources: List[str]


# Habit-based nutrient estimation patterns
HABIT_NUTRIENT_PATTERNS = {
    # Morning habits
    "tea": {"iron": -0.15, "vitamin_b12": 0, "calcium": 0.05},  # Tea inhibits iron absorption
    "coffee": {"iron": -0.1, "vitamin_b12": 0, "calcium": -0.05, "magnesium": -0.1},
    "milk": {"calcium": 0.3, "vitamin_d": 0.15, "protein": 0.15, "vitamin_b12": 0.2},
    "eggs": {"protein": 0.2, "vitamin_b12": 0.25, "vitamin_d": 0.15, "iron": 0.1},
    "fruit": {"vitamin_c": 0.3, "magnesium": 0.1},
    "cereal": {"iron": 0.15, "vitamin_b12": 0.1, "zinc": 0.1},
    "oats": {"iron": 0.15, "magnesium": 0.15, "zinc": 0.1, "protein": 0.1},
    "poha": {"iron": 0.2, "vitamin_b12": 0, "carbohydrates": 0.2},
    "upma": {"iron": 0.1, "protein": 0.1, "carbohydrates": 0.2},
    "idli": {"protein": 0.15, "iron": 0.1, "vitamin_b12": 0.05},
    "dosa": {"protein": 0.1, "iron": 0.1, "vitamin_b12": 0.05},
    "paratha": {"protein": 0.1, "iron": 0.1, "carbohydrates": 0.25},
    "bread": {"iron": 0.08, "protein": 0.05, "carbohydrates": 0.2},
    "skip": {"iron": -0.2, "vitamin_b12": -0.15, "protein": -0.15, "calcium": -0.15},
    "skip breakfast": {"iron": -0.2, "vitamin_b12": -0.15, "protein": -0.15, "calcium": -0.15},
    
    # Afternoon habits
    "rice": {"iron": 0.1, "protein": 0.1, "carbohydrates": 0.3},
    "roti": {"iron": 0.15, "protein": 0.1, "magnesium": 0.1},
    "chapati": {"iron": 0.15, "protein": 0.1, "magnesium": 0.1},
    "dal": {"iron": 0.25, "protein": 0.35, "zinc": 0.15, "magnesium": 0.2},
    "lentils": {"iron": 0.25, "protein": 0.35, "zinc": 0.15, "magnesium": 0.2},
    "vegetables": {"iron": 0.15, "magnesium": 0.2, "vitamin_c": 0.2},
    "salad": {"iron": 0.1, "magnesium": 0.15, "vitamin_c": 0.25},
    "curd": {"calcium": 0.25, "vitamin_b12": 0.15, "protein": 0.15},
    "yogurt": {"calcium": 0.25, "vitamin_b12": 0.15, "protein": 0.15},
    "paneer": {"calcium": 0.3, "protein": 0.25, "vitamin_b12": 0.1},
    "chicken": {"protein": 0.4, "iron": 0.2, "zinc": 0.3, "vitamin_b12": 0.35},
    "fish": {"protein": 0.35, "vitamin_d": 0.3, "vitamin_b12": 0.4, "zinc": 0.2},
    "mutton": {"protein": 0.35, "iron": 0.3, "zinc": 0.35, "vitamin_b12": 0.4},
    "egg curry": {"protein": 0.25, "vitamin_b12": 0.3, "iron": 0.15},
    "fast food": {"iron": -0.1, "zinc": -0.1, "magnesium": -0.15, "protein": 0.1},
    "outside food": {"iron": -0.05, "zinc": -0.05, "magnesium": -0.1},
    
    # Evening habits
    "evening tea": {"iron": -0.1, "calcium": 0.05},
    "snacks": {"magnesium": -0.05, "zinc": -0.05},
    "fruits": {"vitamin_c": 0.25, "magnesium": 0.1},
    "nuts": {"magnesium": 0.25, "zinc": 0.2, "protein": 0.15, "iron": 0.1},
    "light dinner": {"protein": 0.15, "iron": 0.1, "calcium": 0.1},
    "heavy dinner": {"protein": 0.25, "iron": 0.2, "carbohydrates": 0.3},
    "late dinner": {"magnesium": -0.1, "vitamin_d": -0.05},
    "soup": {"protein": 0.1, "iron": 0.1, "magnesium": 0.1},
    "khichdi": {"protein": 0.2, "iron": 0.15, "zinc": 0.1},
    "sabzi": {"iron": 0.15, "magnesium": 0.15, "vitamin_c": 0.1},
    "buttermilk": {"calcium": 0.15, "vitamin_b12": 0.1, "protein": 0.1},
    "lassi": {"calcium": 0.2, "vitamin_b12": 0.1, "protein": 0.15}
}

# Lifestyle factor impacts
LIFESTYLE_IMPACTS = {
    "sedentary": {"vitamin_d": -0.3, "magnesium": -0.2, "calcium": -0.15},
    "desk job": {"vitamin_d": -0.25, "magnesium": -0.15},
    "office work": {"vitamin_d": -0.2, "magnesium": -0.1},
    "active": {"vitamin_d": 0.1, "magnesium": 0.1, "calcium": 0.1},
    "outdoor": {"vitamin_d": 0.3, "magnesium": 0.1},
    "gym": {"protein": 0.1, "magnesium": 0.15, "zinc": 0.1},
    "exercise": {"protein": 0.1, "magnesium": 0.1, "calcium": 0.1},
    "smoking": {"vitamin_c": -0.3, "vitamin_d": -0.2, "calcium": -0.2},
    "alcohol": {"vitamin_b12": -0.25, "magnesium": -0.2, "zinc": -0.15},
    "stress": {"magnesium": -0.25, "vitamin_b12": -0.15, "zinc": -0.1}
}


class NutritionDeficiencyEngine:
    """
    AI-Powered Personalized Nutrition & Deficiency Risk Assessment Engine
    
    Analyzes user data and generates comprehensive deficiency risk assessment
    with WHO benchmark comparisons and geographic risk integration.
    """
    
    def __init__(self, user_data: Dict[str, Any]):
        """Initialize engine with user data"""
        self.user_data = user_data
        self.age = self._parse_numeric(user_data.get("age", 25))
        self.gender = user_data.get("gender", "female")
        self.height_cm = self._parse_numeric(user_data.get("height_cm", 160))
        self.weight_kg = self._parse_numeric(user_data.get("weight_kg", 60))
        self.health_category = user_data.get("health_category", "adult")
        self.dietary_preference = user_data.get("dietary_preference", "vegetarian")
        self.location = user_data.get("location", "")
        self.morning_habits = user_data.get("morning_habits", "")
        self.afternoon_habits = user_data.get("afternoon_habits", "")
        self.evening_habits = user_data.get("evening_habits", "")
        self.questionnaire = user_data.get("questionnaire_responses", {})
        
        # Analysis results
        self.bmi_analysis = {}
        self.deficiency_risks = []
        self.alerts = []
        self.recommendations = []
        self.visualization_data = {}
    
    def _parse_numeric(self, value: Any) -> float:
        """Parse numeric value from various formats"""
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value.replace(",", "").strip())
            except ValueError:
                return 0.0
        return 0.0
    
    def analyze(self) -> Dict[str, Any]:
        """Perform complete deficiency risk analysis"""
        # Step 1: BMI Calculation
        self.bmi_analysis = self._calculate_bmi()
        
        # Step 2: Demographic Risk Mapping
        demographic_risks = self._map_demographic_risks()
        
        # Step 3: Dietary Pattern Analysis
        dietary_estimates = self._analyze_dietary_patterns()
        
        # Step 4: Geographic Risk Integration
        geographic_risks = self._integrate_geographic_risks()
        
        # Step 5: Questionnaire Analysis
        symptom_risks = self._analyze_questionnaire()
        
        # Step 6: Calculate deficiency risks for each nutrient
        self.deficiency_risks = self._calculate_deficiency_risks(
            demographic_risks, dietary_estimates, geographic_risks, symptom_risks
        )
        
        # Step 7: Generate alerts
        self.alerts = self._generate_alerts()
        
        # Step 8: Generate recommendations
        self.recommendations = self._generate_recommendations()
        
        # Step 9: Prepare visualization data
        self.visualization_data = self._prepare_visualization_data()
        
        return self._compile_output()
    
    def _calculate_bmi(self) -> Dict[str, Any]:
        """Calculate BMI and classification"""
        return calculate_bmi(self.weight_kg, self.height_cm)
    
    def _map_demographic_risks(self) -> Dict[str, float]:
        """Map demographic factors to nutrient risk scores"""
        risks = {
            "iron": 0.0,
            "vitamin_b12": 0.0,
            "vitamin_d": 0.0,
            "calcium": 0.0,
            "magnesium": 0.0,
            "zinc": 0.0,
            "protein": 0.0
        }
        
        # Age-based risks
        if self.age < 5:
            risks["iron"] += 15
            risks["zinc"] += 10
            risks["vitamin_d"] += 10
        elif self.age >= 60:
            risks["vitamin_b12"] += 20
            risks["vitamin_d"] += 15
            risks["calcium"] += 15
        elif 14 <= self.age <= 18:
            risks["iron"] += 15
            risks["calcium"] += 10
            risks["zinc"] += 10
        
        # Gender-based risks
        if self.gender.lower() == "female":
            if 14 <= self.age <= 50:
                risks["iron"] += 20  # Menstrual loss
            risks["calcium"] += 10
        
        # Health category risks
        health_cat = self.health_category.lower() if self.health_category else ""
        if "pregnant" in health_cat:
            risks["iron"] += 25
            risks["calcium"] += 15
            risks["vitamin_d"] += 15
            risks["vitamin_b12"] += 15
            risks["protein"] += 15
        elif "lactating" in health_cat:
            risks["calcium"] += 20
            risks["vitamin_d"] += 10
            risks["vitamin_b12"] += 10
            risks["protein"] += 10
        
        # BMI-based risks
        bmi_category = self.bmi_analysis.get("category", "normal")
        if bmi_category == "underweight":
            risks["protein"] += 25
            risks["iron"] += 20
            risks["vitamin_b12"] += 15
            risks["zinc"] += 15
        elif bmi_category == "obese":
            risks["vitamin_d"] += 20  # Fat-soluble vitamin absorption issues
            risks["magnesium"] += 15
        
        # Dietary preference risks
        diet_factors = get_dietary_risk_factors(self.dietary_preference)
        for nutrient in diet_factors.get("high_risk", []):
            multiplier = diet_factors.get("factor_multiplier", {}).get(nutrient, 1.5)
            risks[nutrient] = risks.get(nutrient, 0) + (25 * multiplier)
        for nutrient in diet_factors.get("moderate_risk", []):
            multiplier = diet_factors.get("factor_multiplier", {}).get(nutrient, 1.2)
            risks[nutrient] = risks.get(nutrient, 0) + (15 * multiplier)
        
        return risks
    
    def _analyze_dietary_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Analyze dietary habits and estimate nutrient coverage"""
        nutrient_scores = {
            "iron": {"score": 0.5, "sources": [], "patterns": []},
            "vitamin_b12": {"score": 0.5, "sources": [], "patterns": []},
            "vitamin_d": {"score": 0.5, "sources": [], "patterns": []},
            "calcium": {"score": 0.5, "sources": [], "patterns": []},
            "magnesium": {"score": 0.5, "sources": [], "patterns": []},
            "zinc": {"score": 0.5, "sources": [], "patterns": []},
            "protein": {"score": 0.5, "sources": [], "patterns": []}
        }
        
        # Analyze morning habits
        morning_lower = self.morning_habits.lower() if self.morning_habits else ""
        self._analyze_habit_string(morning_lower, "morning", nutrient_scores)
        
        # Analyze afternoon habits
        afternoon_lower = self.afternoon_habits.lower() if self.afternoon_habits else ""
        self._analyze_habit_string(afternoon_lower, "afternoon", nutrient_scores)
        
        # Analyze evening habits
        evening_lower = self.evening_habits.lower() if self.evening_habits else ""
        self._analyze_habit_string(evening_lower, "evening", nutrient_scores)
        
        # Cap scores between 0.1 and 1.0
        for nutrient in nutrient_scores:
            nutrient_scores[nutrient]["score"] = max(0.1, min(1.0, nutrient_scores[nutrient]["score"]))
        
        return nutrient_scores
    
    def _analyze_habit_string(self, habit_str: str, time_period: str, 
                              nutrient_scores: Dict[str, Dict[str, Any]]) -> None:
        """Analyze a habit string and update nutrient scores"""
        if not habit_str:
            return
        
        for pattern, effects in HABIT_NUTRIENT_PATTERNS.items():
            if pattern in habit_str:
                for nutrient, impact in effects.items():
                    if nutrient in nutrient_scores:
                        nutrient_scores[nutrient]["score"] += impact
                        if impact > 0:
                            nutrient_scores[nutrient]["sources"].append(f"{pattern} ({time_period})")
                        else:
                            nutrient_scores[nutrient]["patterns"].append(f"{pattern} reduces absorption")
        
        # Check lifestyle impacts
        for lifestyle, impacts in LIFESTYLE_IMPACTS.items():
            if lifestyle in habit_str:
                for nutrient, impact in impacts.items():
                    if nutrient in nutrient_scores:
                        nutrient_scores[nutrient]["score"] += impact
                        if impact < 0:
                            nutrient_scores[nutrient]["patterns"].append(f"{lifestyle} lifestyle")
    
    def _integrate_geographic_risks(self) -> Dict[str, float]:
        """Integrate geographic risk factors"""
        geo_risks = {
            "iron": 0.0,
            "vitamin_b12": 0.0,
            "vitamin_d": 0.0,
            "calcium": 0.0,
            "magnesium": 0.0,
            "zinc": 0.0,
            "protein": 0.0
        }
        
        if not self.location:
            # Return default moderate risks for unknown location
            return {k: 10.0 for k in geo_risks}
        
        # Get regional anemia data
        anemia_data = get_regional_anemia_data(self.location)
        anemia_prevalence = anemia_data.get("prevalence", 52.0)
        
        # Scale iron risk based on regional prevalence
        if anemia_prevalence >= 60:
            geo_risks["iron"] += 25
        elif anemia_prevalence >= 50:
            geo_risks["iron"] += 15
        elif anemia_prevalence >= 40:
            geo_risks["iron"] += 10
        
        # Get groundwater data
        water_data = get_groundwater_data(self.location)
        
        # High fluoride can interfere with nutrient absorption
        if water_data.get("fluoride") in ["high", "very_high"]:
            geo_risks["calcium"] += 10
            geo_risks["magnesium"] += 10
        
        # High arsenic areas
        if water_data.get("arsenic") in ["high", "very_high"]:
            geo_risks["iron"] += 10
            geo_risks["zinc"] += 10
        
        # Get vitamin D regional risk
        vit_d_data = get_vitamin_d_regional_risk(self.location)
        vit_d_factor = vit_d_data.get("factor", 1.0)
        geo_risks["vitamin_d"] += (vit_d_factor - 1) * 30
        
        # Urban pattern risks
        if anemia_data.get("urban_rural") == "urban":
            geo_risks["vitamin_d"] += 10
            geo_risks["magnesium"] += 5
        
        return geo_risks
    
    def _analyze_questionnaire(self) -> Dict[str, float]:
        """Analyze questionnaire responses for symptom-based risks"""
        symptom_risks = {
            "iron": 0.0,
            "vitamin_b12": 0.0,
            "vitamin_d": 0.0,
            "calcium": 0.0,
            "magnesium": 0.0,
            "zinc": 0.0,
            "protein": 0.0
        }
        
        q = self.questionnaire
        
        # Fatigue analysis
        fatigue = str(q.get("fatigue", "")).lower()
        if fatigue in ["yes", "severe", "high", "frequent", "always"]:
            symptom_risks["iron"] += 25
            symptom_risks["vitamin_b12"] += 20
            symptom_risks["vitamin_d"] += 15
        elif fatigue in ["moderate", "sometimes", "occasional"]:
            symptom_risks["iron"] += 15
            symptom_risks["vitamin_b12"] += 10
            symptom_risks["vitamin_d"] += 10
        
        # Hair fall analysis
        hair_fall = str(q.get("hair_fall", "")).lower()
        if hair_fall in ["yes", "severe", "high", "frequent", "always"]:
            symptom_risks["iron"] += 20
            symptom_risks["zinc"] += 20
            symptom_risks["protein"] += 15
            symptom_risks["vitamin_d"] += 10
        elif hair_fall in ["moderate", "sometimes", "occasional"]:
            symptom_risks["iron"] += 10
            symptom_risks["zinc"] += 10
            symptom_risks["protein"] += 10
        
        # Muscle cramps analysis
        cramps = str(q.get("muscle_cramps", "")).lower()
        if cramps in ["yes", "severe", "high", "frequent", "always"]:
            symptom_risks["magnesium"] += 25
            symptom_risks["calcium"] += 20
            symptom_risks["vitamin_d"] += 15
        elif cramps in ["moderate", "sometimes", "occasional"]:
            symptom_risks["magnesium"] += 15
            symptom_risks["calcium"] += 10
            symptom_risks["vitamin_d"] += 10
        
        # Sun exposure analysis
        sun_exposure = self._parse_numeric(q.get("sun_exposure_minutes_per_day", 30))
        if sun_exposure < 10:
            symptom_risks["vitamin_d"] += 30
        elif sun_exposure < 20:
            symptom_risks["vitamin_d"] += 20
        elif sun_exposure < 30:
            symptom_risks["vitamin_d"] += 10
        else:
            symptom_risks["vitamin_d"] -= 10
        
        # Dairy servings analysis
        dairy = self._parse_numeric(q.get("dairy_servings_per_day", 1))
        if dairy < 1:
            symptom_risks["calcium"] += 25
            symptom_risks["vitamin_b12"] += 15
            symptom_risks["vitamin_d"] += 10
        elif dairy < 2:
            symptom_risks["calcium"] += 10
            symptom_risks["vitamin_b12"] += 5
        
        # Green leafy vegetables frequency
        greens = self._parse_numeric(q.get("green_leafy_frequency_per_week", 3))
        if greens < 2:
            symptom_risks["iron"] += 20
            symptom_risks["magnesium"] += 15
            symptom_risks["calcium"] += 10
        elif greens < 4:
            symptom_risks["iron"] += 10
            symptom_risks["magnesium"] += 5
        
        # Water source analysis
        water_source = str(q.get("water_source", "")).lower()
        if "bore" in water_source or "ground" in water_source or "well" in water_source:
            symptom_risks["calcium"] += 5  # Hard water can affect absorption
        
        return symptom_risks
    
    def _calculate_deficiency_risks(
        self,
        demographic_risks: Dict[str, float],
        dietary_estimates: Dict[str, Dict[str, Any]],
        geographic_risks: Dict[str, float],
        symptom_risks: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Calculate comprehensive deficiency risk for each nutrient"""
        nutrients = ["iron", "vitamin_b12", "vitamin_d", "calcium", "magnesium", "zinc", "protein"]
        
        nutrient_units = {
            "iron": "mg",
            "vitamin_b12": "mcg",
            "vitamin_d": "IU",
            "calcium": "mg",
            "magnesium": "mg",
            "zinc": "mg",
            "protein": "g"
        }
        
        deficiency_risks = []
        
        for nutrient in nutrients:
            # Get RDA for this user
            rda = get_rda_for_user(nutrient, self.gender, self.age, self.health_category)
            
            # Get dietary score (0.1 to 1.0)
            dietary_score = dietary_estimates.get(nutrient, {}).get("score", 0.5)
            
            # Estimate intake as percentage of RDA
            estimated_coverage = dietary_score * 100
            estimated_intake = rda * dietary_score
            
            # Calculate base probability from all risk sources
            base_probability = (
                demographic_risks.get(nutrient, 0) +
                geographic_risks.get(nutrient, 0) +
                symptom_risks.get(nutrient, 0)
            )
            
            # Adjust based on dietary coverage
            coverage_penalty = max(0, (70 - estimated_coverage) * 0.5)  # Penalty if below 70%
            
            # Calculate final probability
            final_probability = min(100, max(0, base_probability + coverage_penalty))
            
            # Classify risk level
            risk_level = classify_risk_level(final_probability)
            
            # Determine primary causes
            primary_causes = self._determine_primary_causes(
                nutrient, demographic_risks, dietary_estimates, geographic_risks, symptom_risks
            )
            
            # Get symptom links
            symptom_links = self._get_symptom_links(nutrient)
            
            # Get geographic influence
            geo_influence = self._get_geographic_influence(nutrient)
            
            deficiency_risks.append({
                "nutrient": nutrient,
                "risk_level": risk_level,
                "probability_percent": round(final_probability, 1),
                "recommended_intake": f"{rda} {nutrient_units[nutrient]}/day",
                "estimated_intake": f"{round(estimated_intake, 1)} {nutrient_units[nutrient]}/day",
                "coverage_percent": round(estimated_coverage, 1),
                "primary_causes": primary_causes,
                "symptom_links": symptom_links,
                "geographic_influence": geo_influence
            })
        
        # Sort by probability (highest first)
        deficiency_risks.sort(key=lambda x: x["probability_percent"], reverse=True)
        
        return deficiency_risks
    
    def _determine_primary_causes(
        self,
        nutrient: str,
        demographic_risks: Dict[str, float],
        dietary_estimates: Dict[str, Dict[str, Any]],
        geographic_risks: Dict[str, float],
        symptom_risks: Dict[str, float]
    ) -> List[str]:
        """Determine primary causes for a nutrient deficiency risk"""
        causes = []
        
        # Check demographic contribution
        if demographic_risks.get(nutrient, 0) > 15:
            if self.dietary_preference.lower() in ["vegetarian", "vegan"]:
                if nutrient in ["vitamin_b12", "iron", "zinc"]:
                    causes.append(f"{self.dietary_preference} diet limits {nutrient} sources")
            if self.gender.lower() == "female" and nutrient == "iron":
                if 14 <= self.age <= 50:
                    causes.append("Female reproductive age increases iron needs")
            if "pregnant" in str(self.health_category).lower():
                causes.append(f"Pregnancy increases {nutrient} requirements")
            if self.bmi_analysis.get("category") == "underweight":
                if nutrient in ["protein", "iron"]:
                    causes.append("Underweight status suggests inadequate nutrition")
        
        # Check dietary patterns
        dietary_score = dietary_estimates.get(nutrient, {}).get("score", 0.5)
        if dietary_score < 0.5:
            patterns = dietary_estimates.get(nutrient, {}).get("patterns", [])
            for pattern in patterns[:2]:  # Limit to 2 patterns
                causes.append(pattern)
        
        # Check geographic factors
        if geographic_risks.get(nutrient, 0) > 10:
            if nutrient == "iron":
                anemia_data = get_regional_anemia_data(self.location)
                if anemia_data.get("prevalence", 0) > 50:
                    causes.append(f"High regional anemia prevalence ({anemia_data['prevalence']}%)")
            if nutrient == "vitamin_d":
                vit_d_data = get_vitamin_d_regional_risk(self.location)
                causes.append(vit_d_data.get("reason", "Regional environmental factors"))
        
        # Check symptom correlations
        if symptom_risks.get(nutrient, 0) > 15:
            if self.questionnaire.get("fatigue") and nutrient in ["iron", "vitamin_b12", "vitamin_d"]:
                causes.append("Fatigue symptoms reported")
            if self.questionnaire.get("hair_fall") and nutrient in ["iron", "zinc"]:
                causes.append("Hair fall symptoms reported")
            if self.questionnaire.get("muscle_cramps") and nutrient in ["magnesium", "calcium"]:
                causes.append("Muscle cramps reported")
            
            sun_exposure = self._parse_numeric(self.questionnaire.get("sun_exposure_minutes_per_day", 30))
            if nutrient == "vitamin_d" and sun_exposure < 20:
                causes.append(f"Low sun exposure ({sun_exposure} min/day)")
        
        return causes[:5] if causes else ["General dietary assessment"]
    
    def _get_symptom_links(self, nutrient: str) -> List[str]:
        """Get common symptoms linked to nutrient deficiency"""
        symptom_map = {
            "iron": ["Fatigue", "Pale skin", "Brittle nails", "Shortness of breath", "Hair loss"],
            "vitamin_b12": ["Fatigue", "Numbness/tingling", "Memory issues", "Mood changes", "Pale skin"],
            "vitamin_d": ["Bone pain", "Muscle weakness", "Fatigue", "Depression", "Frequent illness"],
            "calcium": ["Muscle cramps", "Brittle nails", "Dental problems", "Osteoporosis risk", "Numbness"],
            "magnesium": ["Muscle cramps", "Fatigue", "Weakness", "Poor sleep", "Headaches"],
            "zinc": ["Hair loss", "Poor wound healing", "Loss of taste/smell", "Skin issues", "Frequent infections"],
            "protein": ["Muscle loss", "Weakness", "Hair loss", "Slow healing", "Edema"]
        }
        return symptom_map.get(nutrient, ["General weakness", "Fatigue"])
    
    def _get_geographic_influence(self, nutrient: str) -> str:
        """Get geographic influence description for nutrient"""
        if not self.location:
            return "Location data unavailable for regional assessment"
        
        influences = []
        
        if nutrient == "iron":
            anemia_data = get_regional_anemia_data(self.location)
            prevalence = anemia_data.get("prevalence", 52)
            severity = anemia_data.get("severity", "moderate")
            influences.append(f"Regional anemia prevalence: {prevalence}% ({severity} severity)")
        
        if nutrient == "vitamin_d":
            vit_d_data = get_vitamin_d_regional_risk(self.location)
            influences.append(vit_d_data.get("reason", "Standard regional exposure"))
        
        if nutrient in ["calcium", "magnesium"]:
            water_data = get_groundwater_data(self.location)
            fluoride = water_data.get("fluoride", "moderate")
            if fluoride in ["high", "very_high"]:
                influences.append(f"High fluoride in groundwater may affect absorption")
            else:
                influences.append(water_data.get("health_impact", "Standard water quality"))
        
        return "; ".join(influences) if influences else f"No specific regional risk for {nutrient}"
    
    def _generate_alerts(self) -> List[Dict[str, Any]]:
        """Generate structured alerts based on risk levels"""
        alerts = []
        
        for risk in self.deficiency_risks:
            nutrient = risk["nutrient"]
            risk_level = risk["risk_level"]
            probability = risk["probability_percent"]
            
            if risk_level == "critical":
                lab_test = get_recommended_test(nutrient)
                alerts.append({
                    "type": "🚨 Critical Alert",
                    "nutrient": nutrient,
                    "message": f"Critical {nutrient} deficiency risk ({probability}%)",
                    "action": f"Recommend: {lab_test['primary']}",
                    "priority": 1
                })
            elif risk_level == "high":
                lab_test = get_recommended_test(nutrient)
                alerts.append({
                    "type": "🔴 High Alert",
                    "nutrient": nutrient,
                    "message": f"High {nutrient} deficiency risk ({probability}%)",
                    "action": f"Consider: {lab_test['primary']}",
                    "priority": 2
                })
            elif risk_level == "moderate":
                alerts.append({
                    "type": "⚠️ Moderate Alert",
                    "nutrient": nutrient,
                    "message": f"Moderate {nutrient} deficiency risk ({probability}%)",
                    "action": "Dietary modification recommended",
                    "priority": 3
                })
        
        # Sort by priority
        alerts.sort(key=lambda x: x["priority"])
        
        return alerts
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Dietary recommendations based on deficiency risks
        food_suggestions = {
            "iron": {
                "vegetarian": ["Spinach", "Lentils", "Chickpeas", "Fortified cereals", "Pumpkin seeds"],
                "non_vegetarian": ["Lean red meat", "Organ meats", "Shellfish", "Spinach", "Legumes"]
            },
            "vitamin_b12": {
                "vegetarian": ["Fortified cereals", "Fortified nutritional yeast", "Dairy products", "Eggs", "Consider B12 supplementation"],
                "non_vegetarian": ["Fish", "Meat", "Eggs", "Dairy", "Shellfish"]
            },
            "vitamin_d": {
                "all": ["Increase sun exposure (15-30 min)", "Fatty fish", "Fortified milk", "Egg yolks", "Mushrooms exposed to sunlight"]
            },
            "calcium": {
                "all": ["Dairy products", "Fortified plant milk", "Leafy greens", "Sesame seeds", "Ragi/Finger millet"]
            },
            "magnesium": {
                "all": ["Nuts (almonds, cashews)", "Seeds", "Whole grains", "Dark chocolate", "Spinach"]
            },
            "zinc": {
                "vegetarian": ["Pumpkin seeds", "Chickpeas", "Cashews", "Fortified cereals", "Yogurt"],
                "non_vegetarian": ["Oysters", "Red meat", "Poultry", "Beans", "Nuts"]
            },
            "protein": {
                "vegetarian": ["Dal/Lentils", "Paneer", "Tofu", "Chickpeas", "Greek yogurt"],
                "non_vegetarian": ["Chicken", "Fish", "Eggs", "Lean meat", "Dairy"]
            }
        }
        
        is_veg = self.dietary_preference.lower() in ["vegetarian", "vegan", "eggetarian"]
        diet_key = "vegetarian" if is_veg else "non_vegetarian"
        
        for risk in self.deficiency_risks:
            if risk["risk_level"] in ["high", "critical", "moderate"]:
                nutrient = risk["nutrient"]
                foods = food_suggestions.get(nutrient, {})
                
                if "all" in foods:
                    food_list = foods["all"]
                else:
                    food_list = foods.get(diet_key, foods.get("vegetarian", []))
                
                recommendations.append({
                    "category": "dietary",
                    "nutrient": nutrient,
                    "priority": "high" if risk["risk_level"] in ["high", "critical"] else "moderate",
                    "foods": food_list,
                    "tip": self._get_dietary_tip(nutrient)
                })
        
        # Lifestyle recommendations
        if self.questionnaire.get("sun_exposure_minutes_per_day"):
            sun_exp = self._parse_numeric(self.questionnaire.get("sun_exposure_minutes_per_day", 30))
            if sun_exp < 20:
                recommendations.append({
                    "category": "lifestyle",
                    "nutrient": "vitamin_d",
                    "priority": "high",
                    "action": "Increase sun exposure to 20-30 minutes daily (10am-3pm)",
                    "tip": "Morning sun is best for vitamin D synthesis without excessive UV damage"
                })
        
        # Tea timing recommendation if detected
        if "tea" in str(self.morning_habits).lower() or "tea" in str(self.evening_habits).lower():
            recommendations.append({
                "category": "lifestyle",
                "nutrient": "iron",
                "priority": "moderate",
                "action": "Avoid tea/coffee with meals - have them 1-2 hours after meals",
                "tip": "Tannins in tea reduce iron absorption by up to 60%"
            })
        
        # Lab test recommendations for high-risk nutrients
        critical_nutrients = [r["nutrient"] for r in self.deficiency_risks if r["risk_level"] == "critical"]
        high_risk_nutrients = [r["nutrient"] for r in self.deficiency_risks if r["risk_level"] == "high"]
        
        if critical_nutrients:
            recommendations.append({
                "category": "medical",
                "priority": "critical",
                "action": "Schedule blood tests for nutrient assessment",
                "tests": [get_recommended_test(n)["primary"] for n in critical_nutrients],
                "tip": "Consult a healthcare provider for proper evaluation"
            })
        elif high_risk_nutrients:
            recommendations.append({
                "category": "medical",
                "priority": "high",
                "action": "Consider routine blood tests",
                "tests": [get_recommended_test(n)["primary"] for n in high_risk_nutrients[:3]],
                "tip": "Annual nutrient screening recommended"
            })
        
        return recommendations
    
    def _get_dietary_tip(self, nutrient: str) -> str:
        """Get a dietary tip for maximizing nutrient absorption"""
        tips = {
            "iron": "Pair iron-rich foods with vitamin C (citrus, tomatoes) to enhance absorption",
            "vitamin_b12": "B12 is mainly from animal sources; vegetarians should consider fortified foods or supplements",
            "vitamin_d": "15-30 minutes of midday sun exposure helps natural vitamin D synthesis",
            "calcium": "Spread calcium intake throughout the day; avoid taking with iron supplements",
            "magnesium": "Soaking nuts and seeds can increase magnesium bioavailability",
            "zinc": "Animal sources have more bioavailable zinc; vegetarians need 50% more",
            "protein": "Combine legumes with grains for complete protein in vegetarian diets"
        }
        return tips.get(nutrient, "Maintain a balanced diet with diverse food sources")
    
    def _prepare_visualization_data(self) -> Dict[str, Any]:
        """Prepare data for dashboard visualization"""
        # Nutrient comparison chart data
        nutrient_comparison = []
        for risk in self.deficiency_risks:
            # Parse numeric values from strings
            rda_str = risk["recommended_intake"].split()[0]
            est_str = risk["estimated_intake"].split()[0]
            
            nutrient_comparison.append({
                "nutrient": risk["nutrient"],
                "who_rda": float(rda_str) if rda_str.replace(".", "").isdigit() else 0,
                "estimated_intake": float(est_str) if est_str.replace(".", "").isdigit() else 0,
                "coverage_percent": risk["coverage_percent"]
            })
        
        # Risk radar chart data
        risk_radar = []
        for risk in self.deficiency_risks:
            risk_radar.append({
                "nutrient": risk["nutrient"],
                "risk_probability": risk["probability_percent"],
                "risk_level": risk["risk_level"]
            })
        
        # Heatmap region flag
        anemia_data = get_regional_anemia_data(self.location) if self.location else {}
        heatmap_flag = "elevated" if anemia_data.get("prevalence", 0) > 50 else "normal"
        
        # Urban trend flag
        urban_flag = anemia_data.get("urban_rural", "mixed")
        
        return {
            "nutrient_comparison_chart": nutrient_comparison,
            "risk_radar_chart": risk_radar,
            "heatmap_region_flag": heatmap_flag,
            "urban_trend_flag": urban_flag
        }
    
    def _compile_output(self) -> Dict[str, Any]:
        """Compile final JSON output"""
        # Generate demographic summary
        demographic_summary = self._generate_demographic_summary()
        
        return {
            "bmi_analysis": self.bmi_analysis,
            "demographic_summary": demographic_summary,
            "deficiency_risks": self.deficiency_risks,
            "alerts": self.alerts,
            "recommendations": self.recommendations,
            "visualization_data": self.visualization_data
        }
    
    def _generate_demographic_summary(self) -> str:
        """Generate a demographic summary string"""
        parts = []
        
        parts.append(f"{self.age}-year-old {self.gender}")
        
        if self.health_category:
            parts.append(f"{self.health_category}")
        
        if self.dietary_preference:
            parts.append(f"{self.dietary_preference} diet")
        
        if self.location:
            parts.append(f"residing in {self.location}")
        
        bmi_category = self.bmi_analysis.get("category", "")
        bmi_value = self.bmi_analysis.get("bmi_value", 0)
        if bmi_category:
            parts.append(f"BMI: {bmi_value} ({bmi_category})")
        
        return ". ".join(parts)


def assess_nutrition_deficiency(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for nutrition deficiency assessment
    
    Args:
        user_data: Dictionary containing user information and questionnaire responses
        
    Returns:
        Structured JSON output with comprehensive deficiency risk assessment
    """
    engine = NutritionDeficiencyEngine(user_data)
    return engine.analyze()
