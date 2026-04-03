import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv("config/.env")  # Load environment variables from .env file

def get_feedback_from_llm(student_data, predicted_status, predicted_salary):

    try:
        # Initialize the LLM (Requires GOOGLE_API_KEY in your environment/.env)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7,transport="rest",convert_system_message_to_human=True)
        
        template = """
        You are an expert career counselor and technical placement guide. 
        
        A student has the following academic profile:
        - Coding Score: {coding_skill_score}/100
        - Aptitude Score: {aptitude_score}/100
        - Internships: {internships_count}
        - Projects: {projects_count}
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
            input_variables=["coding_skill_score", "aptitude_score", "internships_count", "projects_count", "cgpa", "backlogs", "predicted_status", "predicted_salary"],
            template=template
        )
        
        # Format the prompt with the data
        formatted_prompt = prompt.format(
            coding_skill_score=student_data['coding_skill_score'],
            aptitude_score=student_data['aptitude_score'],
            internships_count=student_data['internships_count'],
            projects_count=student_data['projects_count'],
            cgpa=student_data['cgpa'],
            backlogs=student_data['backlogs'],
            predicted_status=predicted_status,
            predicted_salary=predicted_salary
        )
        
        # Call the LLM
        response = llm.invoke(formatted_prompt)
        return response.content
    
    except Exception as e:
        return f"Error generating feedback: {str(e)}"


