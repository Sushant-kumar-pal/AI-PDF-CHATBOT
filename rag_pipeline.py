from langchain_groq import ChatGroq
from vector_database import faiss_db
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st


# Lazily create the Groq model to avoid raising at import time if the API key is missing
def create_llm():
    try:
        return ChatGroq(model="openai/gpt-oss-120b")
    except Exception as e:
        # If called from a Streamlit app, show a helpful error and stop execution
        if 'streamlit' in globals():
            st.error(f"Could not initialize LLM: {e}\nMake sure GROQ_API_KEY is set in your environment.")
            st.stop()
        raise

# Uncomment the following if you're NOT using pipenv
#from dotenv import load_dotenv
#load_dotenv()

#Step1: Setup LLM (Use DeepSeek R1 with Groq)
# Use create_llm() at runtime to initialize the model

#Step2: Retrieve Docs

def retrieve_docs(query):
    return faiss_db.similarity_search(query)

def get_context(documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    return context

#Step3: Answer Question

custom_prompt_template = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context
Question: {question} 
Context: {context} 
Answer:
"""

def answer_query(documents, model, query):
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    chain = prompt | model
    return chain.invoke({"question": query, "context": context})

#question="If a government forbids the right to assemble peacefully which articles are violated and why?"
#retrieved_docs=retrieve_docs(question)