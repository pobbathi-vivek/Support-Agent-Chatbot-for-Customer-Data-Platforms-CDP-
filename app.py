import streamlit as st
import chromadb
import ollama

# List of ChromaDB sources
CHROMA_SOURCES = [
    "chroma_db_lytics",
    "chroma_db_mparticle",
    "chroma_db_zeotap",
    "chroma_db_segment_data"
]

def generate_embedding(text):
    """Generate an embedding for a given text using Ollama."""
    try:
        response = ollama.embeddings(model="mistral", prompt=text)
        return response["embedding"] if "embedding" in response else None
    except Exception as e:
        st.error(f"Error generating embedding: {e}")
        return None


def summarize_text(text):
    """Summarize the retrieved text using Mistral."""
    try:
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": "You are an AI assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following:\n\n{text}"}
            ]
        )
        return response["message"]["content"] if "message" in response else "Summarization failed."
    except Exception as e:
        st.error(f"Error summarizing text: {e}")
        return "Summarization failed."


def query_chroma(query, top_k=5):
    """Search for relevant text snippets across all ChromaDB sources."""
    query_embedding = generate_embedding(query)
    if not query_embedding:
        st.error("Failed to generate embedding for query.")
        return None

    all_texts = []
    all_metadata = []

    for source in CHROMA_SOURCES:
        try:
            chroma_client = chromadb.PersistentClient(path=f"./{source}")
            collection = chroma_client.get_collection(name="web_scrape_data")
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            if results["ids"]:
                retrieved_texts = [metadata["text"] for metadata in results["metadatas"][0]]
                all_texts.extend(retrieved_texts)
                all_metadata.extend(results["metadatas"][0])
        except Exception as e:
            st.error(f"Error querying {source}: {e}")

    if not all_texts:
        st.warning("No matching results found across all sources.")
        return None

    summary = summarize_text("\n\n".join(all_texts))
    return summary, all_metadata


# Streamlit UI
def main():
    st.title("Support Agent Chatbot for CDP")
    st.write("Ask questions based on the scraped website data from multiple sources.")

    query = st.text_input("Enter your query:")
    if st.button("Search") and query:
        with st.spinner("Searching across all sources..."):
            summary, results = query_chroma(query)

            if summary:
                st.subheader("Summary of Retrieved Information:")
                st.write(summary)

                st.subheader("Retrieved Results:")
                for i, metadata in enumerate(results):
                    st.markdown(f"*Result {i+1}:*")
                    st.markdown(f"🔗 *URL:* {metadata['url']}")
                    st.markdown(f"📝 *Text:* {metadata['text'][:500]}...")


if __name__ == "__main__":
    main()
