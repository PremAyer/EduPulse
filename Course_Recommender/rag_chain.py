from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

def get_rag_chain(retriever):
    """Sets up the LLM and the Retrieval QA Chain."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    system_prompt = (""" You are an expert career counselor for EduPulse. 
    Your goal is to provide a comprehensive learning roadmap by combining institutional course data with high-quality free resources.

    Instructions:
    1. Primary Context: Use the provided context below to suggest relevant paid courses from the EduPulse database.
    2. YouTube Integration: If a user specifically asks for 'free' courses, or if no free options exist in the context, you MUST provide 2-3 specific, high-quality YouTube channels or tutorial series (e.g., 'Krish Naik' or 'CampusX' for Data Science, 'FreeCodeCamp' for General Tech).
    3. Hybrid Learning Path: Structure your response as a 'Learning Path' that shows how free YouTube tutorials can supplement the core courses found in the database.
    4. Behavior: Even if the context says 'no free courses', do NOT say "there are no free options." Instead, provide the YouTube alternatives immediately.
    5. Tone: Be encouraging, professional, and concise.

    Context: {context}
    """)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain