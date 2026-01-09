from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.3
)

prompt = PromptTemplate(
    input_variables=["life_stage", "status", "region"],
    template="""
You are an AI nutrition assistant.

User life stage: {life_stage}
User region: {region}
Nutrient deficiency status: {status}

Explain in simple, non-medical language:
- Which nutrients are low
- Why this matters for this life stage
- General food-based suggestions common in this region

Rules:
- Do NOT diagnose disease
- Do NOT suggest medicines
- Keep explanation concise and friendly
- End with a short safety disclaimer
"""
)

def generate_explainable_advice(life_stage, status, region):
    formatted_prompt = prompt.format(
        life_stage=life_stage,
        status=str(status),
        region=region
    )
    response = llm.invoke(formatted_prompt)
    return response.content
