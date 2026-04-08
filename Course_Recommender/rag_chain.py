from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

def get_rag_chain(retriever):
    """Sets up the LLM and the Retrieval QA Chain."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    system_prompt = (""" You are an expert career counselor for EduPulse. 
                     Use the following pieces of retrieved context to recommend courses:
                    {context}

                   Special Instructions:
                   1. If the user asks for free options, specifically recommend 2-3 high-quality YouTube channels or specific tutorial series relevant to their query (e.g., 'Programming with Mosh' for Web Dev, or 'Krish Naik' for Data Science).
                   2. Always provide a 'Learning Path' that combines the paid courses found in our database with these free YouTube resources.
                   3. Be encouraging and concise.
                   "Context: {context}"""  
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain