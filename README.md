
# 🩺 MediAssist – AI-Powered Medical Research Assistant

MediAssist is an AI-powered medical research assistant that retrieves relevant scientific research articles from PubMed, stores and indexes them in ChromaDB, and generates context-aware answers using Large Language Models (LLMs).

Built using **LangGraph, LangChain, PubMed API, ChromaDB, Hugging Face Embeddings, Groq and Streamlit**, MediAssist demonstrates a Retrieval-Augmented Generation (RAG) pipeline for medical research assistance.

---

## 🚀 Features

- **PubMed Integration:** Search and retrieve medical research articles and abstracts directly from PubMed.
- **Automated Document Processing:** Convert retrieved research articles into structured LangChain documents.
- **Vector Database:** Store and retrieve medical research documents using ChromaDB.
- **Semantic Search:** Retrieve relevant research articles based on user queries.
- **LLM-Powered Responses:** Generate context-aware answers using Groq-hosted LLMs.
- **LangGraph Workflow:** Manage document retrieval and answer generation through a graph-based architecture.
- **Interactive UI:** Ask medical research questions through a Streamlit interface.
- **Research References:** Display retrieved articles with their PubMed IDs and direct links.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| LLM | Llama 3.3 70B Versatile (Groq) |
| LLM Framework | LangChain |
| Orchestration | LangGraph |
| Embeddings | Sentence Transformers |
| Embedding Model | all-mpnet-base-v2 |
| Vector Database | ChromaDB |
| Research Data Source | PubMed E-utilities API |
| Frontend | Streamlit |
| Environment Management | Python Dotenv |

---

## 🏗️ Architecture

```text
                 User
                  |
                  v
          Streamlit Interface
                  |
                  v
            User Question
                  |
                  v
          LangGraph Workflow
                  |
          +-------+-------+
          |               |
          v               |
      PubMed API           |
          |               |
          v               |
    Article Retrieval      |
          |               |
          v               |
    Abstract Extraction   |
          |               |
          v               |
   LangChain Documents    |
          |               |
          v               |
       ChromaDB            |
          |               |
          v               |
    Semantic Retrieval    |
          |               |
          +-------+-------+
                  |
                  v
             Groq LLM
                  |
                  v
          Generated Answer
                  |
                  v
          Streamlit Output
```

---

## 📂 Project Structure

```text
MediAssist/
│
├── server.py              # LangGraph backend and RAG pipeline
├── app.py                 # Streamlit frontend
├── pubmed.py              # PubMed article retrieval
├── .env                   # API credentials
├── requirements.txt       # Project dependencies
│
└── resources/
    └── VectoreStore/      # Persistent ChromaDB storage
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/MediAssist.git

cd MediAssist
```

### 2. Create a Virtual Environment

Using Python 3.12:

```bash
py -3.12 -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from:

https://console.groq.com/keys

### 5. Run the Backend

Test the LangGraph workflow:

```bash
python server.py
```

### 6. Run the Streamlit Application

```bash
streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

---

## 🔄 Workflow

### 1. User Query
The user enters a medical research question through the Streamlit interface.

### 2. PubMed Retrieval
The PubMed E-utilities API searches for relevant scientific articles using the user's query.

### 3. Document Processing
Retrieved article abstracts are converted into structured LangChain Document objects with metadata such as:
- PMID
- Title
- Journal
- Authors
- Publication Date

### 4. Vector Storage
Hugging Face Sentence Transformer embeddings convert documents into numerical vectors, which are stored in ChromaDB.

### 5. Semantic Retrieval
ChromaDB retrieves the most relevant research documents based on semantic similarity.

### 6. Answer Generation
The retrieved research context and user question are passed to the Groq-hosted LLM.

### 7. Response Generation
MediAssist generates an answer and displays the retrieved research references in Streamlit.

---

## 🧠 LangGraph Workflow

The application uses a two-node LangGraph workflow.

```text
          START
            |
            v
      Load_documents
            |
            v
      Generate_answer
            |
            v
           END
```

**Load_documents**
- Search PubMed.
- Fetch article abstracts.
- Convert articles into LangChain documents.
- Store documents in ChromaDB.
- Retrieve relevant documents.

**Generate_answer**
- Receive retrieved research context.
- Construct the LLM prompt.
- Generate a research-based answer using Groq.

---

## 📚 Data Source

**PubMed – National Library of Medicine**

PubMed provides access to biomedical and life sciences literature.

- Website: https://pubmed.ncbi.nlm.nih.gov/
- API Documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/

MediAssist uses the following E-utilities endpoints:

- ESearch: Search PubMed articles.
- EFetch: Retrieve article metadata and abstracts.

---

## 🔮 Future Enhancements

- [ ] Advanced query expansion for better PubMed retrieval.
- [ ] Improved document chunking and indexing.
- [ ] Incremental document ingestion.
- [ ] Hybrid search using semantic and keyword retrieval.
- [ ] Reranking retrieved research articles.
- [ ] Citation-aware answer generation.
- [ ] Conversation history and memory.
- [ ] Multi-agent medical research workflows.
- [ ] Research paper summarization.
- [ ] Deploy the application to Streamlit Community Cloud.

---

## ⚠️ Disclaimer

MediAssist is designed for educational and medical research purposes only.

It does not provide medical diagnoses, treatment recommendations, or professional medical advice.

Always consult a qualified healthcare professional for medical decisions.

---

## 👨‍💻 Author

**Trijesh Kondapuram**

B.Tech – Artificial Intelligence & Data Science

- GitHub: https://github.com/trijesh61
- LinkedIn: Add your LinkedIn profile URL

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub!
