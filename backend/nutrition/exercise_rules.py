def get_exercise_plan(life_stage, risk_level):
    if life_stage == "pregnant":
        if risk_level == "HIGH":
            return {
                "type": "Light activity",
                "examples": ["Slow walking", "Prenatal stretching"],
                "duration": "10–15 minutes",
                "intensity": "Low",
                "notes": "Focus on gentle movement and rest"
            }
        elif risk_level == "MEDIUM":
            return {
                "type": "Moderate activity",
                "examples": ["Walking", "Prenatal yoga"],
                "duration": "20–30 minutes",
                "intensity": "Moderate",
                "notes": "Avoid overexertion"
            }
        else:
            return {
                "type": "Regular prenatal exercise",
                "examples": ["Walking", "Light yoga"],
                "duration": "30 minutes",
                "intensity": "Moderate",
                "notes": "Maintain consistency"
            }

    # Non-pregnant adults
    if risk_level == "HIGH":
        return {
            "type": "Low-impact activity",
            "examples": ["Walking", "Stretching"],
            "duration": "15–20 minutes",
            "intensity": "Low",
            "notes": "Focus on recovery"
        }

    if risk_level == "MEDIUM":
        return {
            "type": "Balanced activity",
            "examples": ["Brisk walking", "Yoga"],
            "duration": "30 minutes",
            "intensity": "Moderate",
            "notes": "Consistency matters"
        }

    return {
        "type": "Active routine",
        "examples": ["Jogging", "Strength training"],
        "duration": "45 minutes",
        "intensity": "Moderate–High",
        "notes": "Maintain balanced nutrition"
    }
