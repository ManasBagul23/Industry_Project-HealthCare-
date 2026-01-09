from datetime import date, timedelta
from .models import FoodLog

def extract_user_features(user, days=7):
    start_date = date.today() - timedelta(days=days)
    logs = FoodLog.objects.filter(user=user, date__gte=start_date)

    if not logs.exists():
        return None

    iron = calcium = protein = 0.0
    days_logged = set()

    for log in logs:
        factor = log.quantity / 100
        iron += log.food.iron * factor
        calcium += log.food.calcium * factor
        protein += log.food.protein * factor
        days_logged.add(log.date)

    return {
        "avg_iron": round(iron / days, 2),
        "avg_calcium": round(calcium / days, 2),
        "avg_protein": round(protein / days, 2),
        "consistency": round(len(days_logged) / days, 2)
    }
