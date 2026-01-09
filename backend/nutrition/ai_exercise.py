from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.3
)

prompt = PromptTemplate(
    input_variables=[
        "life_stage",
        "risk_level",
        "exercise_plan",
        "region"
    ],
    template="""
You are an AI health assistant.

User life stage: {life_stage}
Nutrition risk level: {risk_level}
Exercise plan: {exercise_plan}
User region: {region}

Explain in simple, supportive language:
- Why this type of exercise is suitable
- How it helps given the risk level
- General safety reminders

Rules:
- Do NOT give medical advice
- Do NOT suggest new exercises
- Do NOT change intensity or duration
- Keep explanation short and reassuring
- End with a safety disclaimer
"""
)

def explain_exercise(life_stage, risk_level, exercise_plan, region):
    text = prompt.format(
        life_stage=life_stage,
        risk_level=risk_level,
        exercise_plan=str(exercise_plan),
        region=region
    )
    response = llm.invoke(text)
    return response.content
