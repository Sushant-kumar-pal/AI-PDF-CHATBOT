import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq


# =========================
# LOAD ENV
# =========================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()


# =========================
# CONFIG
# =========================
EMBED_MODEL = "nomic-embed-text"
PDF_DIR = "pdfs"
os.makedirs(PDF_DIR, exist_ok=True)


# =========================
# PROMPT TEMPLATE
# =========================
CUSTOM_PROMPT = """
You are an AI Lawyer assistant.

Use ONLY the provided context to answer the question.
If the answer is not in the context, say:
"I don't know based on the provided document."

Do not make up information.

Question:
{question}

Context:
{context}

Answer:
"""


# =========================
# LLM (Groq)
# =========================
def create_llm():
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="openai/gpt-oss-120b",
        temperature=0
    )


# =========================
# FILE HANDLING
# =========================
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(PDF_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    return loader.load()


# =========================
# TEXT SPLITTING
# =========================
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_documents(documents)


# =========================
# EMBEDDINGS (Ollama Local)
# =========================
def get_embedding_model():
    return OllamaEmbeddings(model=EMBED_MODEL)


# =========================
# VECTOR STORE (IN-MEMORY)
# =========================
def create_vector_store(chunks):
    embeddings = get_embedding_model()
    db = FAISS.from_documents(chunks, embeddings)
    return db


def retrieve_context(db, query):
    docs = db.similarity_search(query, k=4)
    return "\n\n".join([doc.page_content for doc in docs])


# =========================
# ANSWER GENERATION
# =========================
def generate_answer(query, context):
    llm = create_llm()
    prompt = ChatPromptTemplate.from_template(CUSTOM_PROMPT)
    chain = prompt | llm
    response = chain.invoke({"question": query, "context": context})
    return response.content


# =========================
# STREAMLIT UI
# =========================
st.title("AI Reasoning Chatbot")
st.write("Upload a legal PDF and ask questions about it.")

uploaded_file = st.file_uploader("Upload a Legal PDF", type="pdf")
user_query = st.text_area("Ask a question about the document:")

if uploaded_file:

    # Rebuild DB only when new PDF uploaded
    if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:

        with st.spinner("Processing document..."):

            file_path = save_uploaded_file(uploaded_file)
            documents = load_pdf(file_path)
            chunks = split_documents(documents)

            st.session_state.db = create_vector_store(chunks)
            st.session_state.current_file = uploaded_file.name

        st.success("Document processed successfully!")

if st.button("Ask AI Lawyer"):

    if not uploaded_file or not user_query:
        st.error("Please upload a PDF and enter a question.")
        st.stop()

    with st.spinner("Generating answer..."):

        context = retrieve_context(st.session_state.db, user_query)
        answer = generate_answer(user_query, context)

    st.chat_message("user").write(user_query)
    st.chat_message("assistant").write(answer)