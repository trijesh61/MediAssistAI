
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langgraph.graph import StateGraph, START, END

from pubmed import PubMedRetriever

load_dotenv()

# ==============================
# CONFIGURATION
# ==============================

llm = None
Vector_db = None

Vector_db_Path = Path(__file__).parent / "resources" / "VectoreStore"
collection_name = "medical_data"
llm_name = "openai/gpt-oss-120b"


# ==============================
# INITIALIZE COMPONENTS
# ==============================

def initialize_components():

    global llm, Vector_db

    if llm is None:
        llm = ChatGroq(
            model=llm_name,
            temperature=0.2,
            max_tokens=500
        )

    if Vector_db is None:

        ef = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        Vector_db = Chroma(
            collection_name=collection_name,
            embedding_function=ef,
            persist_directory=str(Vector_db_Path)
        )


# ==============================
# LANGGRAPH STATE
# ==============================

class MediAssist(TypedDict, total=False):
    question: str
    context: list[Document]
    answer: str


# ==============================
# NODE 1: LOAD DOCUMENTS
# ==============================

def load_documents(state: MediAssist):

    initialize_components()

    question = state["question"]

    print("Searching PubMed...")

    pmid_list = PubMedRetriever.search_pubmed_articles(
        search_term=question,
        max_results=30
    )

    if not pmid_list:
        return {"context": []}

    articles = PubMedRetriever.fetch_pubmed_abstracts(pmid_list)

    documents = []

    for article in articles:

        abstract_text = "\n".join(
            f"{section}: {content}"
            for section, content in article["abstract"].items()
        )

        page_content = f"""
Title: {article['title']}

Abstract:
{abstract_text}

Journal: {article['journal']}
Publication Date: {article['publication_date']}
Authors: {article['authors']}
"""

        documents.append(
            Document(
                page_content=page_content,
                metadata={
                    "pmid": article["pmid"],
                    "title": article["title"],
                    "journal": article["journal"],
                    "publication_date": article["publication_date"],
                    "authors": article["authors"],
                    "source": "PubMed"
                }
            )
        )

    # Avoid duplicate PMID insertion
    existing_ids = set(Vector_db.get()["ids"])

    new_documents = [
        doc for doc in documents
        if doc.metadata["pmid"] not in existing_ids
    ]

    if new_documents:

        Vector_db.add_documents(
            documents=new_documents,
            ids=[doc.metadata["pmid"] for doc in new_documents]
        )

    # Retrieve relevant articles
    relevant_docs = Vector_db.similarity_search(
        query=question,
        k=3
    )

    return {"context": relevant_docs}


# ==============================
# NODE 2: GENERATE ANSWER
# ==============================

def generate_answer(state: MediAssist):

    initialize_components()

    question = state["question"]
    context = state.get("context", [])

    # Limit total research context
    context_text = "\n\n".join(
        doc.page_content[:800]
        for doc in context[:3]
    )

    # Additional strict limit
    context_text = context_text[:2500]

    if not context_text.strip():

        return {
            "answer": "No relevant PubMed research articles were found. Please try another question."
        }

    prompt = f"""
You are MediAssist, a medical research assistant.

Answer using only the provided PubMed research context.

Instructions:
- Explain findings in simple language.
- Do not invent medical facts.
- Do not invent citations.
- Mention limitations if evidence is insufficient.
- This is educational information, not a substitute for medical advice.

Research Context:
{context_text}

Question:
{question}

Answer:
"""

    print("Generating answer...")
    print("Prompt length:", len(prompt))

    response = llm.invoke(prompt)

    return {"answer": response.content}


# ==============================
# LANGGRAPH
# ==============================

graph = StateGraph(MediAssist)

graph.add_node("Load_documents", load_documents)
graph.add_node("Generate_answer", generate_answer)

graph.add_edge(START, "Load_documents")
graph.add_edge("Load_documents", "Generate_answer")
graph.add_edge("Generate_answer", END)

app = graph.compile()


# ==============================
# TEST SERVER
# ==============================

if __name__ == "__main__":

    question = "What are the common symptoms of diabetes?"

    initialize_components()

    result = app.invoke({
        "question": question
    })

    print("\nQUESTION:", question)
    print("\nANSWER:", result["answer"])

    print("\nRETRIEVED ARTICLES:")

    for doc in result.get("context", []):
        print(
            doc.metadata.get("pmid"),
            doc.metadata.get("title")
        )
