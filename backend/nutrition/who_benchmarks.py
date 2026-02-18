"""
WHO and Government Recommended Daily Allowance (RDA) Benchmarks
Based on WHO guidelines and Indian Council of Medical Research (ICMR) standards
"""

# Age-Gender specific RDA values (per day)
WHO_RDA_BENCHMARKS = {
    "iron": {  # mg/day
        "male": {
            "child_1_3": 7,
            "child_4_8": 10,
            "child_9_13": 8,
            "adolescent_14_18": 11,
            "adult_19_50": 8,
            "adult_51_plus": 8
        },
        "female": {
            "child_1_3": 7,
            "child_4_8": 10,
            "child_9_13": 8,
            "adolescent_14_18": 15,
            "adult_19_50": 18,
            "adult_51_plus": 8,
            "pregnant": 27,
            "lactating": 9
        }
    },
    "vitamin_b12": {  # mcg/day
        "male": {
            "child_1_3": 0.9,
            "child_4_8": 1.2,
            "child_9_13": 1.8,
            "adolescent_14_18": 2.4,
            "adult_19_50": 2.4,
            "adult_51_plus": 2.4
        },
        "female": {
            "child_1_3": 0.9,
            "child_4_8": 1.2,
            "child_9_13": 1.8,
            "adolescent_14_18": 2.4,
            "adult_19_50": 2.4,
            "adult_51_plus": 2.4,
            "pregnant": 2.6,
            "lactating": 2.8
        }
    },
    "vitamin_d": {  # IU/day
        "male": {
            "child_1_3": 600,
            "child_4_8": 600,
            "child_9_13": 600,
            "adolescent_14_18": 600,
            "adult_19_50": 600,
            "adult_51_plus": 800
        },
        "female": {
            "child_1_3": 600,
            "child_4_8": 600,
            "child_9_13": 600,
            "adolescent_14_18": 600,
            "adult_19_50": 600,
            "adult_51_plus": 800,
            "pregnant": 600,
            "lactating": 600
        }
    },
    "calcium": {  # mg/day
        "male": {
            "child_1_3": 700,
            "child_4_8": 1000,
            "child_9_13": 1300,
            "adolescent_14_18": 1300,
            "adult_19_50": 1000,
            "adult_51_plus": 1200
        },
        "female": {
            "child_1_3": 700,
            "child_4_8": 1000,
            "child_9_13": 1300,
            "adolescent_14_18": 1300,
            "adult_19_50": 1000,
            "adult_51_plus": 1200,
            "pregnant": 1000,
            "lactating": 1300
        }
    },
    "magnesium": {  # mg/day
        "male": {
            "child_1_3": 80,
            "child_4_8": 130,
            "child_9_13": 240,
            "adolescent_14_18": 410,
            "adult_19_50": 400,
            "adult_51_plus": 420
        },
        "female": {
            "child_1_3": 80,
            "child_4_8": 130,
            "child_9_13": 240,
            "adolescent_14_18": 360,
            "adult_19_50": 310,
            "adult_51_plus": 320,
            "pregnant": 350,
            "lactating": 310
        }
    },
    "zinc": {  # mg/day
        "male": {
            "child_1_3": 3,
            "child_4_8": 5,
            "child_9_13": 8,
            "adolescent_14_18": 11,
            "adult_19_50": 11,
            "adult_51_plus": 11
        },
        "female": {
            "child_1_3": 3,
            "child_4_8": 5,
            "child_9_13": 8,
            "adolescent_14_18": 9,
            "adult_19_50": 8,
            "adult_51_plus": 8,
            "pregnant": 11,
            "lactating": 12
        }
    },
    "protein": {  # g/day (0.8g per kg body weight as baseline)
        "male": {
            "child_1_3": 13,
            "child_4_8": 19,
            "child_9_13": 34,
            "adolescent_14_18": 52,
            "adult_19_50": 56,
            "adult_51_plus": 56
        },
        "female": {
            "child_1_3": 13,
            "child_4_8": 19,
            "child_9_13": 34,
            "adolescent_14_18": 46,
            "adult_19_50": 46,
            "adult_51_plus": 46,
            "pregnant": 71,
            "lactating": 71
        }
    }
}

# BMI Classification
BMI_CATEGORIES = {
    "underweight": {"min": 0, "max": 18.5},
    "normal": {"min": 18.5, "max": 24.9},
    "overweight": {"min": 25, "max": 29.9},
    "obese": {"min": 30, "max": 100}
}

# Risk probability thresholds
RISK_THRESHOLDS = {
    "low": {"min": 0, "max": 30},
    "moderate": {"min": 31, "max": 60},
    "high": {"min": 61, "max": 80},
    "critical": {"min": 81, "max": 100}
}


def get_age_category(age: int) -> str:
    """Determine age category based on age"""
    if age <= 3:
        return "child_1_3"
    elif age <= 8:
        return "child_4_8"
    elif age <= 13:
        return "child_9_13"
    elif age <= 18:
        return "adolescent_14_18"
    elif age <= 50:
        return "adult_19_50"
    else:
        return "adult_51_plus"


def get_rda_for_user(nutrient: str, gender: str, age: int, 
                     health_category: str = None) -> float:
    """
    Get recommended daily allowance for a specific nutrient
    based on gender, age, and health category
    """
    gender_key = gender.lower() if gender.lower() in ["male", "female"] else "female"
    
    # Handle pregnancy/lactating status
    if health_category:
        health_lower = health_category.lower()
        if health_lower == "pregnant":
            if gender_key == "female":
                return WHO_RDA_BENCHMARKS.get(nutrient, {}).get("female", {}).get("pregnant", 
                       WHO_RDA_BENCHMARKS.get(nutrient, {}).get("female", {}).get("adult_19_50", 0))
        elif health_lower == "lactating":
            if gender_key == "female":
                return WHO_RDA_BENCHMARKS.get(nutrient, {}).get("female", {}).get("lactating",
                       WHO_RDA_BENCHMARKS.get(nutrient, {}).get("female", {}).get("adult_19_50", 0))
    
    age_category = get_age_category(age)
    return WHO_RDA_BENCHMARKS.get(nutrient, {}).get(gender_key, {}).get(age_category, 0)


def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    """Calculate BMI and return category classification"""
    if height_cm <= 0 or weight_kg <= 0:
        return {"bmi_value": 0, "category": "unknown", "interpretation": "Invalid measurements"}
    
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    category = "normal"
    interpretation = ""
    
    if bmi < 18.5:
        category = "underweight"
        interpretation = "BMI indicates underweight status. May indicate nutritional deficiency risk, particularly for protein, iron, and B-vitamins."
    elif bmi < 25:
        category = "normal"
        interpretation = "BMI is within healthy range. Focus on maintaining balanced nutrition."
    elif bmi < 30:
        category = "overweight"
        interpretation = "BMI indicates overweight status. May benefit from dietary modifications and increased physical activity."
    else:
        category = "obese"
        interpretation = "BMI indicates obesity. Higher risk for certain nutrient deficiencies despite excess caloric intake."
    
    return {
        "bmi_value": round(bmi, 2),
        "category": category,
        "interpretation": interpretation
    }


def classify_risk_level(probability_percent: float) -> str:
    """Classify risk level based on probability percentage"""
    if probability_percent <= 30:
        return "low"
    elif probability_percent <= 60:
        return "moderate"
    elif probability_percent <= 80:
        return "high"
    else:
        return "critical"


def get_alert_type(risk_level: str) -> str:
    """Get alert emoji/type based on risk level"""
    alert_map = {
        "low": "✅ Low Risk",
        "moderate": "⚠️ Moderate Alert",
        "high": "🔴 High Alert",
        "critical": "🚨 Critical – Recommend laboratory test"
    }
    return alert_map.get(risk_level, "⚠️ Alert")
