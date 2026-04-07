from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

def get_rag_chain(retriever):
    """Sets up the LLM and the Retrieval QA Chain."""
    # Initialize Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    system_prompt = (
        "You are an expert academic advisor. "
        "Use the following pieces of retrieved course context to recommend the best "
        "options to the user. Do not make up any courses. Only recommend from the provided context.\n"
        "Explain WHY each course fits their specific request based on duration, level, or price.\n\n"
        "Context: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    # Combine documents and LLM
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain