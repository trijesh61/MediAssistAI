
import streamlit as st
from server import app

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="MediAssist",
    page_icon="🩺",
    layout="wide"
)

# ==============================
# HEADER
# ==============================

st.title("🩺 MediAssist")

st.markdown(
    "### AI-Powered Medical Research Assistant"
)

st.caption(
    "Powered by PubMed | LangGraph | ChromaDB | Groq"
)

st.divider()

# ==============================
# USER INPUT
# ==============================

question = st.text_area(
    "Ask your medical research question",
    placeholder="Example: What are the common symptoms of diabetes?",
    height=120
)

ask_button = st.button(
    "🔍 Search & Generate Answer",
    type="primary",
    use_container_width=True
)

# ==============================
# PROCESS QUESTION
# ==============================

if ask_button:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner(
                "Searching PubMed and generating your answer..."
            ):

                result = app.invoke({
                    "question": question
                })

            # ANSWER
            st.success("Research completed!")

            st.subheader("💡 MediAssist Answer")

            st.markdown(result.get("answer", "No answer generated."))

            st.divider()

            # SOURCES
            st.subheader("📚 Retrieved PubMed Articles")

            documents = result.get("context", [])

            if documents:

                for index, doc in enumerate(documents, 1):

                    title = doc.metadata.get(
                        "title",
                        "Research Article"
                    )

                    with st.expander(f"{index}. {title}"):

                        st.write(doc.page_content)

                        st.caption(
                            f"PMID: {doc.metadata.get('pmid', 'N/A')}"
                        )

                        st.caption(
                            f"Journal: {doc.metadata.get('journal', 'N/A')}"
                        )

                        st.caption(
                            f"Publication Year: {doc.metadata.get('publication_date', 'N/A')}"
                        )

                        pmid = doc.metadata.get("pmid")

                        if pmid:
                            st.link_button(
                                "View on PubMed",
                                f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                            )

            else:

                st.info("No relevant research articles found.")

        except Exception as e:

            st.error(f"Something went wrong: {e}")

# ==============================
# FOOTER
# ==============================

st.divider()

st.caption(
    "MediAssist | AI-powered Medical Research Assistant"
)

st.caption(
    "For educational and research purposes only. "
    "Always consult qualified healthcare professionals."
)
