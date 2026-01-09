# Location-Based Nutrition & Exercise Recommendation System (Backend)

## Overview
This project is a **backend system** for a women-focused nutrition and exercise recommendation platform.  
It provides **location-based**, **life-stage-aware**, and **personalized** recommendations using a combination of:
- Rule-based nutritional logic
- Machine Learning for risk prediction
- Explainable AI (LangChain + Groq)

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

| Endpoint | Description |
|--------|------------|
| `/accounts/login/` | User login (JWT) |
| `/accounts/profile/` | User profile (age, life stage, location) |
| `/nutrition/food/` | Food item management |
| `/nutrition/log/` | Daily food logging |
| `/nutrition/deficiency/` | Nutrition deficiency + regional suggestions |
| `/nutrition/risk/` | ML-based nutrition risk prediction |
| `/nutrition/exercise/` | Exercise recommendation + AI explanation |

---

## Environment Setup

Create a `.env` file in the backend root:

```env
GROQ_API_KEY=your_groq_api_key_here
