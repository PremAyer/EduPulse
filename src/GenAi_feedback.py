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

    template = """
You are an expert career counselor and technical placement guide. 

A student has the following academic profile:
- Coding Score: {coding_score}/100
- Aptitude Score: {aptitude_score}/100
- Internships: {internships}
- Projects: {projects}
- CGPA: {cgpa}/10.0
- Active Backlogs: {backlogs}

Our Machine Learning model predicts this student will be: **{predicted_status}**.
Estimated Salary Package: **{predicted_salary} LPA**.

Based on their profile and this prediction, write a supportive, personalized 1-2 paragraph response to the student. 
- If they are predicted to be placed, congratulate them and tell them what their strongest assets are.
- If they are NOT predicted to be placed, empathize, and critically analyze their profile to pinpoint exactly what they are lacking (e.g., high backlogs, low coding score, lack of projects) and give actionable advice on how to improve.

Keep the tone encouraging, professional, and clear.
"""

    prompt = PromptTemplate(
        input_variables=["coding_score", "aptitude_score", "internships_count", "projects_count", "cgpa", "backlogs", "predicted_status", "predicted_salary"],
        template=template
    )

    # Format the prompt with the data
    formatted_prompt = prompt.format(
        coding_score=student_data['coding_score'],
        aptitude_score=student_data['aptitude_score'],
        internships=student_data['internships_count'],
        projects=student_data['projects_count'],
        cgpa=student_data['cgpa'],
        backlogs=student_data['backlogs'],
        predicted_status=predicted_status,
        predicted_salary=predicted_salary
    )

    # Call the Hugging Face model
    response = llm.invoke(formatted_prompt)

    # HuggingFaceEndpoint usually returns the raw text string directly
    return response


        


