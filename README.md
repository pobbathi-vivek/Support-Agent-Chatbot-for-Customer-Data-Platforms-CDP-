# Support Agent Chatbot for CDP

## Overview
This repository contains the Support Agent Chatbot for Customer Data Platforms (CDP), designed to query and summarize information from multiple CDP documentation sources using AI models.

## Features
- Queries multiple CDP documentation websites.
- Retrieves relevant text snippets using ChromaDB.
- Generates text embeddings with the Mistral language model.
- Provides concise summaries using Ollama API.
- User-friendly Streamlit interface.

## Prerequisites
Ensure you have the following installed:
- Python 3.9 or higher
- Git
- Virtual Environment (optional but recommended)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/support-agent-chatbot-cdp.git
   cd support-agent-chatbot-cdp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate    # For Windows
   ```

3. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Required Libraries
The following libraries will be installed via `requirements.txt`:
- streamlit
- chromadb
- ollama
- beautifulsoup4
- requests

## Download Models
The chatbot uses the **Mistral** model through the **Ollama API**. Install Ollama and download the model:
1. Install Ollama from [Ollama's Website](https://ollama.ai/download).
2. Download the Mistral model:
   ```bash
   ollama pull mistral
   ```

## How to Run
1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser at http://localhost:8501

## Project Structure
```
.
├── app.py               # Main Streamlit app
├── requirements.txt     # Required libraries
├── chroma_db_lytics     # ChromaDB collection for Lytics
├── chroma_db_mparticle  # ChromaDB collection for mParticle
├── chroma_db_zeotap     # ChromaDB collection for Zeotap
├── chroma_db_segment_data # ChromaDB collection for Segment
├── scraper and vector db builder # Python script for scraping and vector DB creation
├── sublinks_lytics       # Sublinks text file for Lytics
├── sublinks_mparticle    # Sublinks text file for mParticle
├── sublinks_segment      # Sublinks text file for Segment
└── sublinks_zeotap       # Sublinks text file for Zeotap
└── README.md            # Documentation
```

## Troubleshooting
- If Ollama API fails, ensure it is running in the background.
- Check that all required libraries are installed.
- Verify ChromaDB collections are present in their respective folders.

## Contributing
Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss the proposed changes.

## License
This project is licensed under the MIT License.

