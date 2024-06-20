import chromadb
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from typing import Dict

def query(question: str):
    """
    Queries the system

    Args:
        question: user question
    """

    client = chromadb.PersistentClient(path="./data/chroma_db")

    collection = client.get_or_create_collection("my-papers")

    results = collection.query(
        query_texts=[question],
        n_results=5,
        include=['distances', 'metadatas', 'documents']
    )

    __llmCall(__buildPrompt(question, results))


def __buildPrompt(question: str, results: Dict):
    """
    Builds the prompt for the LLM

    Args:
        question: user question
        results: documents retrieved by index search

    Returns:
        str: built prompt
    """

    prompt = f"User question: {question}\n\nRelavantDocuments:\n"

    for distance, metadata, document in zip(results['distances'][0],results['metadatas'][0],results['documents'][0]):
        if distance > 1:
            break
        if 'image' in metadata.keys():
            continue
        prompt += f"########################################\n{'\n'.join([f"{key}: {value}" for key, value in metadata.items()])}\n{document}\n\n"

    return prompt


def __llmCall(prompt: str):
    """
    Generates and prints the answer using the LLM.

    Args:
        prompt: prompt used as input for the LLM
    """

    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(prompt)

    print(result.content)
