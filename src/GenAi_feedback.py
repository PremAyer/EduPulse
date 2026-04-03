from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
import os


def get_feedback_from_llm(student_data, predicted_status, predicted_salary):
# Initialize the Hugging Face LLM (Mistral-7B is a great free model)
# This requires HUGGINGFACEHUB_API_TOKEN in your environment or .env file
    llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
    max_new_tokens=300,
    temperature=0.7,
    )
    
