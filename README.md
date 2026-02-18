# Location-Based Nutrition & Exercise Recommendation System (Backend)

## Overview
This project is a **backend system** for a women-focused nutrition and exercise recommendation platform.  
It provides **location-based**, **life-stage-aware**, and **personalized** recommendations using a combination of:
- Rule-based nutritional logic
- Machine Learning for risk prediction
- Explainable AI (LangChain + Groq)
- **AI-Powered Micronutrient Deficiency Risk Assessment Engine**

The backend was implemented as part of an industry-oriented academic project.

---

## Key Features

### 1. Location-Based Recommendations
- Uses **state → region mapping** (e.g., West India, North India)
- Provides **regional food suggestions** based on cultural availability
- No Google Maps or paid APIs used (privacy-safe & cost-free)

### 2. Nutrition Deficiency Detection
- Calculates daily nutrient intake (Iron, Calcium, Protein)
- Uses RDA-based rules for life stages
- Supports **pregnancy mode**

### 3. ML-Based Personalization
- Logistic Regression model
- Predicts nutrition risk level (LOW / MEDIUM / HIGH)
- Provides confidence score
- Uses historical food intake data

### 4. Exercise Recommendations
- Rule-based, pregnancy-safe exercise plans
- Adjusted using ML risk level
- No medical advice or unsafe routines

### 5. Explainable AI
- Integrated using **LangChain + Groq**
- Generates human-readable explanations for:
  - Nutrition deficiencies
  - Exercise recommendations
- AI is used only for explanation, not decision-making

### 6. Security & Safety
- JWT-based authentication
- Clear medical disclaimers
- Graceful fallback if AI service is unavailable

### 7. AI-Powered Micronutrient Deficiency Risk Assessment Engine 🆕

A comprehensive, evidence-based nutrition assessment system that provides:

#### Features:
- **BMI Calculation & Classification** - Underweight/Normal/Overweight/Obese with health interpretation
- **Demographic Risk Mapping** - Age, gender, BMI, lifestyle, and health category analysis
- **Dietary Pattern Analysis** - Morning/afternoon/evening habit parsing with nutrient estimation
- **Geographic Risk Integration** - Regional anemia prevalence data (NFHS-5), groundwater mineral imbalances
- **WHO Benchmark Comparison** - RDA vs estimated intake with coverage percentages
- **Risk Classification Model**:
  - 0–30% → Low Risk
  - 31–60% → Moderate Risk
  - 61–80% → High Risk
  - 81–100% → Critical Risk
- **Alert System** - ✅ Low, ⚠️ Moderate, 🔴 High, 🚨 Critical with lab test recommendations
- **Visualization-Ready Data** - Bar charts, radar charts, heatmap flags for dashboard integration

#### Nutrients Assessed:
- Iron
- Vitamin B12
- Vitamin D
- Calcium
- Magnesium
- Zinc
- Protein

#### Intelligence Rules:
- Vegetarian + low dairy → escalated B12 risk
- Fatigue + low iron intake → increased iron probability
- Sun exposure < 20 min/day → Vitamin D high risk
- Tea > 2 cups/day → iron absorption penalty factor
- BMI underweight → protein and iron probability increase
- Region with high anemia prevalence → iron risk boost

---

## Tech Stack

- Backend Framework: **Django + Django REST Framework**
- Database: **PostgreSQL**
- Authentication: **JWT**
- Machine Learning: **scikit-learn**
- AI Explainability: **LangChain + Groq (LLaMA 3.1)**
- Environment Management: **python-dotenv**

---

## API Endpoints (Backend)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/accounts/login/` | POST | User login (JWT) |
| `/accounts/profile/` | GET/POST | User profile (age, life stage, location) |
| `/nutrition/food/` | GET/POST | Food item management |
| `/nutrition/log/` | GET/POST | Daily food logging |
| `/nutrition/deficiency/` | GET | Nutrition deficiency + regional suggestions |
| `/nutrition/risk/` | GET | ML-based nutrition risk prediction |
| `/nutrition/exercise/` | GET | Exercise recommendation + AI explanation |
| `/nutrition/assessment/` | POST | **AI-Powered Deficiency Risk Assessment** (anonymous) |
| `/nutrition/assessment/` | GET | **AI-Powered Deficiency Risk Assessment** (authenticated) |
| `/nutrition/assessment/auth/` | POST | **Assessment with profile + questionnaire** (authenticated) |

---

## AI-Powered Assessment API

### POST `/nutrition/assessment/`

**Input Format:**
```json
{
  "age": "28",
  "gender": "female",
  "height_cm": "160",
  "weight_kg": "55",
  "health_category": "adult",
  "dietary_preference": "vegetarian",
  "location": "Maharashtra",
  "morning_habits": "tea, skip breakfast",
  "afternoon_habits": "rice, dal, vegetables",
  "evening_habits": "light dinner, evening tea",
  "questionnaire_responses": {
    "fatigue": "yes",
    "hair_fall": "moderate",
    "muscle_cramps": "no",
    "sun_exposure_minutes_per_day": "15",
    "dairy_servings_per_day": "1",
    "green_leafy_frequency_per_week": "3",
    "water_source": "municipal"
  }
}
```

**Output Format:**
```json
{
  "bmi_analysis": {
    "bmi_value": 21.48,
    "category": "normal",
    "interpretation": "BMI is within healthy range..."
  },
  "demographic_summary": "28-year-old female. adult. vegetarian diet. residing in Maharashtra. BMI: 21.48 (normal)",
  "deficiency_risks": [
    {
      "nutrient": "iron",
      "risk_level": "critical",
      "probability_percent": 100,
      "recommended_intake": "18 mg/day",
      "estimated_intake": "5.4 mg/day",
      "coverage_percent": 30.0,
      "primary_causes": ["vegetarian diet limits iron sources", "Female reproductive age increases iron needs"],
      "symptom_links": ["Fatigue", "Pale skin", "Brittle nails"],
      "geographic_influence": "Regional anemia prevalence: 48.0% (moderate severity)"
    }
  ],
  "alerts": [
    {
      "type": "🚨 Critical Alert",
      "nutrient": "iron",
      "message": "Critical iron deficiency risk (100%)",
      "action": "Recommend: Complete Blood Count (CBC) with Serum Ferritin",
      "priority": 1
    }
  ],
  "recommendations": [
    {
      "category": "dietary",
      "nutrient": "iron",
      "priority": "high",
      "foods": ["Spinach", "Lentils", "Chickpeas", "Fortified cereals", "Pumpkin seeds"],
      "tip": "Pair iron-rich foods with vitamin C to enhance absorption"
    }
  ],
  "visualization_data": {
    "nutrient_comparison_chart": [...],
    "risk_radar_chart": [...],
    "heatmap_region_flag": "normal",
    "urban_trend_flag": "mixed"
  }
}
```

---

## Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ManasBagul23/Industry_Project-HealthCare-.git
cd Industry_Project-HealthCare-
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your credentials
# - GROQ_API_KEY (get from https://console.groq.com/)
# - Database credentials (if using PostgreSQL)
```

### 5. Database Setup
```bash
cd backend

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 6. Train ML Model (if needed)
```bash
python -c "from nutrition.ml_train import *"
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

---

## Project Structure (Key Files)

```
backend/
├── nutrition/
│   ├── views.py                 # API views including assessment endpoints
│   ├── urls.py                  # URL routing
│   ├── serializers.py           # Input/output validation serializers
│   ├── models.py                # Database models
│   ├── deficiency_engine.py     # 🆕 Core AI assessment engine
│   ├── who_benchmarks.py        # 🆕 WHO RDA standards & BMI calculations
│   ├── geographic_risk.py       # 🆕 Regional health data (NFHS-5, groundwater)
│   ├── regional_foods.py        # Regional food recommendations
│   ├── regions.py               # State to region mapping
│   ├── ai_langchain.py          # LangChain AI explanations
│   ├── ml_predict.py            # ML risk prediction
│   ├── ml_features.py           # Feature extraction
│   └── exercise_rules.py        # Exercise recommendation logic
├── accounts/
│   ├── models.py                # User profile models
│   ├── views.py                 # Auth & profile endpoints
│   └── serializers.py           # User serializers
└── backend/
    └── settings.py              # Django settings
```

---

## Data Sources

The AI-Powered Assessment Engine uses evidence-based data from:

| Data Type | Source |
|-----------|--------|
| WHO RDA Benchmarks | World Health Organization dietary guidelines |
| Regional Anemia Prevalence | NFHS-5 (National Family Health Survey 2019-21) |
| Groundwater Mineral Data | Central Ground Water Board of India |
| Vitamin D Regional Risk | Latitude-based exposure studies |
| Symptom-Nutrient Correlations | Clinical nutrition research |

---

## Testing the Assessment API

You can test the API using curl or any API client:

```bash
curl -X POST http://localhost:8000/nutrition/assessment/ \
  -H "Content-Type: application/json" \
  -d '{
    "age": "28",
    "gender": "female",
    "height_cm": "160",
    "weight_kg": "55",
    "health_category": "adult",
    "dietary_preference": "vegetarian",
    "location": "Maharashtra",
    "morning_habits": "tea, skip breakfast",
    "afternoon_habits": "rice, dal, vegetables",
    "evening_habits": "light dinner",
    "questionnaire_responses": {
      "fatigue": "yes",
      "hair_fall": "moderate",
      "sun_exposure_minutes_per_day": "15",
      "dairy_servings_per_day": "1"
    }
  }'
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Manas Bagul**
- GitHub: [@ManasBagul23](https://github.com/ManasBagul23)

---

## Disclaimer

This system is for **educational and informational purposes only**. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for any health concerns.