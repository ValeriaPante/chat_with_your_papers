# Chat with Your Paper: A RAG System for Research Paper Exploration
This repository implements "Chat with Your Paper" a system that allows you to converse with your favorite research papers through a Retrieval-Augmented Generation (RAG) approach.

**What is Chat with Your Paper?**
Imagine having a casual conversation with a research paper, asking it questions and getting clear and concise answers based on its content. The idea came to me because sometimes I found it difficult to find the paper where I read a particular item. This application makes it possible to retrieve it and find any relevant info!

This system leverages the power of large language models (LLMs) to understand and respond to your queries about a research paper you provide.

Here's how it works:

1. Upload your paper: Provide your favorite research paper in a PDF format
2. Retrieval: The system retrieves relevant sections of the paper based on your query.
3. Generation: The LLM generates a response to your query using the augmented information.

This repository provides the codebase for building the "Chat with Your Paper" system in the *backend* folder. The app notebook instead shows you how to use it.

#### Tech insights
The system is based on two components:
- Search Index, which is used to store the documents which are chunked and embedded. I opted for **chromadb**
- LLM, which generates an asnwer to the user questions using the retrieved info from the index. I opted for **Google Gemini**


