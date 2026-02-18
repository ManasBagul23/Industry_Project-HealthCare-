"""
Geographic Risk Data for Nutrition Deficiency Assessment
Based on NFHS (National Family Health Survey) data and regional health surveys
"""

# Region-based anemia prevalence rates (percentage)
# Source: NFHS-5 (2019-21) and state health surveys
REGIONAL_ANEMIA_PREVALENCE = {
    # North India
    "Delhi": {"prevalence": 52.0, "urban_rural": "urban", "severity": "high"},
    "Punjab": {"prevalence": 46.3, "urban_rural": "mixed", "severity": "moderate"},
    "Haryana": {"prevalence": 54.4, "urban_rural": "mixed", "severity": "high"},
    "Uttar Pradesh": {"prevalence": 50.4, "urban_rural": "mixed", "severity": "high"},
    "Rajasthan": {"prevalence": 54.4, "urban_rural": "mixed", "severity": "high"},
    "Madhya Pradesh": {"prevalence": 53.0, "urban_rural": "mixed", "severity": "high"},
    "Uttarakhand": {"prevalence": 43.6, "urban_rural": "mixed", "severity": "moderate"},
    "Himachal Pradesh": {"prevalence": 40.5, "urban_rural": "rural", "severity": "moderate"},
    "Jammu and Kashmir": {"prevalence": 48.0, "urban_rural": "mixed", "severity": "moderate"},
    
    # West India
    "Maharashtra": {"prevalence": 48.0, "urban_rural": "mixed", "severity": "moderate"},
    "Gujarat": {"prevalence": 62.6, "urban_rural": "mixed", "severity": "critical"},
    "Goa": {"prevalence": 39.2, "urban_rural": "urban", "severity": "moderate"},
    
    # South India
    "Tamil Nadu": {"prevalence": 53.2, "urban_rural": "mixed", "severity": "high"},
    "Kerala": {"prevalence": 36.3, "urban_rural": "mixed", "severity": "moderate"},
    "Karnataka": {"prevalence": 47.8, "urban_rural": "mixed", "severity": "moderate"},
    "Andhra Pradesh": {"prevalence": 58.0, "urban_rural": "mixed", "severity": "high"},
    "Telangana": {"prevalence": 57.6, "urban_rural": "mixed", "severity": "high"},
    
    # East India
    "West Bengal": {"prevalence": 60.7, "urban_rural": "mixed", "severity": "critical"},
    "Odisha": {"prevalence": 64.3, "urban_rural": "mixed", "severity": "critical"},
    "Bihar": {"prevalence": 63.5, "urban_rural": "mixed", "severity": "critical"},
    "Jharkhand": {"prevalence": 65.3, "urban_rural": "mixed", "severity": "critical"},
    "Assam": {"prevalence": 66.4, "urban_rural": "mixed", "severity": "critical"},
    
    # Northeast India
    "Meghalaya": {"prevalence": 56.0, "urban_rural": "rural", "severity": "high"},
    "Manipur": {"prevalence": 39.0, "urban_rural": "mixed", "severity": "moderate"},
    "Mizoram": {"prevalence": 35.0, "urban_rural": "mixed", "severity": "moderate"},
    "Nagaland": {"prevalence": 28.0, "urban_rural": "rural", "severity": "low"},
    "Tripura": {"prevalence": 54.0, "urban_rural": "mixed", "severity": "high"},
    "Arunachal Pradesh": {"prevalence": 42.0, "urban_rural": "rural", "severity": "moderate"},
    "Sikkim": {"prevalence": 34.0, "urban_rural": "rural", "severity": "moderate"},
    
    # Central India
    "Chhattisgarh": {"prevalence": 60.0, "urban_rural": "mixed", "severity": "critical"}
}

# Groundwater mineral imbalances by region
# Based on Central Ground Water Board data
GROUNDWATER_MINERAL_DATA = {
    "Delhi": {
        "fluoride": "high",
        "arsenic": "moderate",
        "iron": "moderate",
        "nitrate": "high",
        "hardness": "high",
        "health_impact": "Dental fluorosis risk, potential thyroid issues"
    },
    "Punjab": {
        "fluoride": "moderate",
        "arsenic": "moderate",
        "iron": "low",
        "nitrate": "high",
        "hardness": "moderate",
        "health_impact": "Agricultural nitrate contamination common"
    },
    "Gujarat": {
        "fluoride": "very_high",
        "arsenic": "low",
        "iron": "moderate",
        "nitrate": "moderate",
        "hardness": "high",
        "health_impact": "Severe fluorosis endemic areas"
    },
    "Rajasthan": {
        "fluoride": "very_high",
        "arsenic": "low",
        "iron": "low",
        "nitrate": "high",
        "hardness": "very_high",
        "health_impact": "Fluorosis belt, hard water common"
    },
    "West Bengal": {
        "fluoride": "moderate",
        "arsenic": "very_high",
        "iron": "high",
        "nitrate": "moderate",
        "hardness": "moderate",
        "health_impact": "Arsenic contamination in groundwater, iron toxicity risk"
    },
    "Bihar": {
        "fluoride": "moderate",
        "arsenic": "high",
        "iron": "high",
        "nitrate": "moderate",
        "hardness": "moderate",
        "health_impact": "Arsenic belt along Ganga plains"
    },
    "Andhra Pradesh": {
        "fluoride": "high",
        "arsenic": "low",
        "iron": "moderate",
        "nitrate": "high",
        "hardness": "high",
        "health_impact": "Fluoride endemic zones"
    },
    "Tamil Nadu": {
        "fluoride": "moderate",
        "arsenic": "low",
        "iron": "low",
        "nitrate": "moderate",
        "hardness": "high",
        "health_impact": "Hard water belt, affects calcium absorption"
    },
    "Karnataka": {
        "fluoride": "high",
        "arsenic": "low",
        "iron": "moderate",
        "nitrate": "moderate",
        "hardness": "moderate",
        "health_impact": "Fluorosis in certain districts"
    },
    "Maharashtra": {
        "fluoride": "moderate",
        "arsenic": "low",
        "iron": "moderate",
        "nitrate": "moderate",
        "hardness": "moderate",
        "health_impact": "Generally acceptable water quality"
    },
    "Kerala": {
        "fluoride": "low",
        "arsenic": "low",
        "iron": "high",
        "nitrate": "low",
        "hardness": "low",
        "health_impact": "High iron content in some areas"
    },
    "Odisha": {
        "fluoride": "moderate",
        "arsenic": "moderate",
        "iron": "high",
        "nitrate": "moderate",
        "hardness": "moderate",
        "health_impact": "Iron contamination common"
    }
}

# Vitamin D deficiency prevalence by region (considering latitude and urban patterns)
VITAMIN_D_REGIONAL_RISK = {
    # Northern states (less sun exposure in winters, more indoor work)
    "Delhi": {"risk_level": "high", "factor": 1.3, "reason": "Urban indoor lifestyle, pollution reducing UV"},
    "Punjab": {"risk_level": "moderate", "factor": 1.1, "reason": "Seasonal variation in sun exposure"},
    "Haryana": {"risk_level": "moderate", "factor": 1.1, "reason": "Mixed urban-rural pattern"},
    "Uttar Pradesh": {"risk_level": "moderate", "factor": 1.15, "reason": "Large population with varied exposure"},
    
    # Western states
    "Maharashtra": {"risk_level": "moderate", "factor": 1.2, "reason": "High urbanization in Mumbai, Pune"},
    "Gujarat": {"risk_level": "moderate", "factor": 1.0, "reason": "Good sun exposure but indoor work common"},
    
    # Southern states (more sun exposure but cultural factors)
    "Tamil Nadu": {"risk_level": "moderate", "factor": 1.0, "reason": "Good sun availability"},
    "Kerala": {"risk_level": "low", "factor": 0.9, "reason": "Adequate sun exposure, coastal lifestyle"},
    "Karnataka": {"risk_level": "moderate", "factor": 1.15, "reason": "Bangalore IT sector indoor work"},
    "Andhra Pradesh": {"risk_level": "moderate", "factor": 1.0, "reason": "Mixed exposure patterns"},
    
    # Eastern states
    "West Bengal": {"risk_level": "high", "factor": 1.25, "reason": "High vegetarian population, less fortified foods"},
    "Odisha": {"risk_level": "moderate", "factor": 1.05, "reason": "Rural areas have better exposure"},
    "Bihar": {"risk_level": "high", "factor": 1.2, "reason": "Indoor work patterns, dietary limitations"},
    
    # Default for unknown regions
    "default": {"risk_level": "moderate", "factor": 1.1, "reason": "National average applied"}
}

# Urban dietary deficiency patterns
URBAN_DEFICIENCY_PATTERNS = {
    "processed_food_high": {
        "risk_nutrients": ["magnesium", "zinc", "vitamin_b12", "iron"],
        "description": "High processed food consumption depletes micronutrients"
    },
    "skip_breakfast": {
        "risk_nutrients": ["vitamin_b12", "iron", "protein", "calcium"],
        "description": "Breakfast skipping common in urban rush"
    },
    "late_night_eating": {
        "risk_nutrients": ["vitamin_d", "magnesium"],
        "description": "Disrupted circadian rhythm affects nutrient metabolism"
    },
    "fast_food_dependent": {
        "risk_nutrients": ["zinc", "magnesium", "vitamin_b12", "calcium"],
        "description": "Fast food lacks essential micronutrients"
    },
    "sedentary_lifestyle": {
        "risk_nutrients": ["vitamin_d", "magnesium", "calcium"],
        "description": "Lack of outdoor activity and movement"
    },
    "high_stress_job": {
        "risk_nutrients": ["magnesium", "vitamin_b12", "zinc"],
        "description": "Stress depletes B-vitamins and magnesium"
    }
}

# Dietary preference risk factors
DIETARY_RISK_FACTORS = {
    "vegetarian": {
        "high_risk": ["vitamin_b12", "iron", "zinc"],
        "moderate_risk": ["protein"],
        "factor_multiplier": {"vitamin_b12": 1.8, "iron": 1.4, "zinc": 1.3, "protein": 1.2}
    },
    "vegan": {
        "high_risk": ["vitamin_b12", "iron", "zinc", "calcium"],
        "moderate_risk": ["protein", "vitamin_d"],
        "factor_multiplier": {"vitamin_b12": 2.5, "iron": 1.5, "zinc": 1.4, "calcium": 1.5, "protein": 1.3, "vitamin_d": 1.3}
    },
    "non_vegetarian": {
        "high_risk": [],
        "moderate_risk": ["magnesium"],
        "factor_multiplier": {"magnesium": 1.1}
    },
    "pescatarian": {
        "high_risk": [],
        "moderate_risk": ["zinc", "magnesium"],
        "factor_multiplier": {"zinc": 1.1, "magnesium": 1.1}
    },
    "eggetarian": {
        "high_risk": ["vitamin_b12"],
        "moderate_risk": ["iron", "zinc"],
        "factor_multiplier": {"vitamin_b12": 1.4, "iron": 1.2, "zinc": 1.2}
    }
}

# Symptom to nutrient correlation matrix
SYMPTOM_NUTRIENT_CORRELATION = {
    "fatigue": {
        "primary": ["iron", "vitamin_b12", "vitamin_d"],
        "secondary": ["magnesium", "protein"],
        "weight": {"iron": 0.4, "vitamin_b12": 0.3, "vitamin_d": 0.2, "magnesium": 0.1}
    },
    "hair_fall": {
        "primary": ["iron", "zinc", "protein"],
        "secondary": ["vitamin_d", "vitamin_b12"],
        "weight": {"iron": 0.35, "zinc": 0.25, "protein": 0.2, "vitamin_d": 0.1, "vitamin_b12": 0.1}
    },
    "muscle_cramps": {
        "primary": ["magnesium", "calcium", "vitamin_d"],
        "secondary": ["potassium"],
        "weight": {"magnesium": 0.4, "calcium": 0.3, "vitamin_d": 0.2, "potassium": 0.1}
    },
    "bone_pain": {
        "primary": ["vitamin_d", "calcium"],
        "secondary": ["magnesium"],
        "weight": {"vitamin_d": 0.45, "calcium": 0.4, "magnesium": 0.15}
    },
    "weakness": {
        "primary": ["iron", "vitamin_b12", "protein"],
        "secondary": ["vitamin_d", "calcium"],
        "weight": {"iron": 0.3, "vitamin_b12": 0.25, "protein": 0.2, "vitamin_d": 0.15, "calcium": 0.1}
    },
    "pale_skin": {
        "primary": ["iron", "vitamin_b12"],
        "secondary": [],
        "weight": {"iron": 0.6, "vitamin_b12": 0.4}
    },
    "brittle_nails": {
        "primary": ["iron", "zinc"],
        "secondary": ["protein", "calcium"],
        "weight": {"iron": 0.4, "zinc": 0.3, "protein": 0.15, "calcium": 0.15}
    },
    "poor_wound_healing": {
        "primary": ["zinc", "protein", "vitamin_c"],
        "secondary": ["iron"],
        "weight": {"zinc": 0.4, "protein": 0.3, "vitamin_c": 0.2, "iron": 0.1}
    },
    "mood_changes": {
        "primary": ["vitamin_d", "vitamin_b12", "magnesium"],
        "secondary": ["iron"],
        "weight": {"vitamin_d": 0.35, "vitamin_b12": 0.3, "magnesium": 0.25, "iron": 0.1}
    },
    "numbness_tingling": {
        "primary": ["vitamin_b12"],
        "secondary": ["calcium", "magnesium"],
        "weight": {"vitamin_b12": 0.6, "calcium": 0.2, "magnesium": 0.2}
    }
}

# Recommended lab tests by nutrient
RECOMMENDED_LAB_TESTS = {
    "iron": {
        "primary": "Complete Blood Count (CBC) with Serum Ferritin",
        "secondary": "Serum Iron, TIBC (Total Iron Binding Capacity)",
        "description": "Ferritin is the most sensitive marker for iron stores"
    },
    "vitamin_b12": {
        "primary": "Serum Vitamin B12",
        "secondary": "Methylmalonic Acid (MMA), Homocysteine",
        "description": "MMA is more accurate for tissue-level B12 status"
    },
    "vitamin_d": {
        "primary": "25-Hydroxy Vitamin D (25-OH Vitamin D)",
        "secondary": "Parathyroid Hormone (PTH)",
        "description": "25-OH Vitamin D is the standard marker"
    },
    "calcium": {
        "primary": "Serum Calcium, Ionized Calcium",
        "secondary": "PTH, Vitamin D",
        "description": "Ionized calcium is more accurate than total calcium"
    },
    "magnesium": {
        "primary": "Serum Magnesium",
        "secondary": "RBC Magnesium",
        "description": "RBC magnesium reflects intracellular stores better"
    },
    "zinc": {
        "primary": "Serum Zinc",
        "secondary": "Alkaline Phosphatase",
        "description": "Serum zinc can be affected by recent meals"
    },
    "protein": {
        "primary": "Serum Total Protein, Albumin",
        "secondary": "Prealbumin, Transferrin",
        "description": "Albumin reflects protein status over weeks"
    }
}


def get_regional_anemia_data(location: str) -> dict:
    """Get anemia prevalence data for a location"""
    # Try exact match first
    if location in REGIONAL_ANEMIA_PREVALENCE:
        return REGIONAL_ANEMIA_PREVALENCE[location]
    
    # Try partial match
    location_lower = location.lower()
    for state, data in REGIONAL_ANEMIA_PREVALENCE.items():
        if state.lower() in location_lower or location_lower in state.lower():
            return data
    
    # Default national average
    return {
        "prevalence": 52.0,
        "urban_rural": "mixed",
        "severity": "moderate"
    }


def get_groundwater_data(location: str) -> dict:
    """Get groundwater mineral data for a location"""
    if location in GROUNDWATER_MINERAL_DATA:
        return GROUNDWATER_MINERAL_DATA[location]
    
    location_lower = location.lower()
    for state, data in GROUNDWATER_MINERAL_DATA.items():
        if state.lower() in location_lower or location_lower in state.lower():
            return data
    
    # Default - moderate levels
    return {
        "fluoride": "moderate",
        "arsenic": "low",
        "iron": "moderate",
        "nitrate": "moderate",
        "hardness": "moderate",
        "health_impact": "Regional data unavailable, using national baseline"
    }


def get_vitamin_d_regional_risk(location: str) -> dict:
    """Get vitamin D risk factor for a location"""
    if location in VITAMIN_D_REGIONAL_RISK:
        return VITAMIN_D_REGIONAL_RISK[location]
    
    location_lower = location.lower()
    for state, data in VITAMIN_D_REGIONAL_RISK.items():
        if state.lower() in location_lower or location_lower in state.lower():
            return data
    
    return VITAMIN_D_REGIONAL_RISK["default"]


def get_dietary_risk_factors(dietary_preference: str) -> dict:
    """Get risk factors based on dietary preference"""
    diet_lower = dietary_preference.lower() if dietary_preference else "non_vegetarian"
    
    for diet, factors in DIETARY_RISK_FACTORS.items():
        if diet in diet_lower or diet_lower in diet:
            return factors
    
    # Default to non-vegetarian baseline
    return DIETARY_RISK_FACTORS["non_vegetarian"]


def get_symptom_correlations(symptoms: list) -> dict:
    """Get nutrient correlations based on symptoms"""
    correlations = {}
    
    for symptom in symptoms:
        symptom_lower = symptom.lower().replace(" ", "_")
        for symptom_key, data in SYMPTOM_NUTRIENT_CORRELATION.items():
            if symptom_key in symptom_lower or symptom_lower in symptom_key:
                for nutrient, weight in data["weight"].items():
                    if nutrient not in correlations:
                        correlations[nutrient] = 0
                    correlations[nutrient] += weight
    
    return correlations


def get_recommended_test(nutrient: str) -> dict:
    """Get recommended lab test for a nutrient"""
    return RECOMMENDED_LAB_TESTS.get(nutrient, {
        "primary": "Comprehensive metabolic panel",
        "secondary": "Consult healthcare provider",
        "description": "General screening recommended"
    })
