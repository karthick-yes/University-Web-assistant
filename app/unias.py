import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
import qdrant_client
from httpx import Timeout
import os
import argparse
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate

load_dotenv()

max_len = 100
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input
    if validate_input_length(user_input):

        generate_text(user_input)
        print(f"user input: {user_input}")
    else:
        raise ValueError(f"the input is longer than the expected limt {max_len}")

# initialise the embedding model
def initialize_embeddings(model_name="sentence-transformers/all-mpnet-base-v2"):
    """initialize the embedding model."""
    return HuggingFaceEmbeddings(model_name = model_name)
# initialise the vector store client
def initialize_qdrant_client():
    """initialize the qdrant client."""
    return qdrant_client.QdrantClient(
        url=os.getenv('qdrant_host'),
        api_key=os.getenv('qdrant_api_key'),
        timeout=Timeout(timeout=None)
    )
#initialise the document store for langchain
def initialize_document_store(client = initialize_qdrant_client(), embeddings = initialize_embeddings(), collection_name="University_Assistant"):
    """initialize the document store."""
    doc_store = Qdrant(client=client, collection_name=collection_name, embeddings=embeddings)
    Doc_store = doc_store.as_retriever()
    return Doc_store
#validate the input length
def validate_input_length(user_prompt: str) -> bool:
    return len(user_prompt) <= max_len
#hard-coded template
def hard_template():
    template = """you are a helpful ai assistant.
answer based on the context provided.you need not look for the exact similarity from the context.
context: {context}
input: {input}
answer: 
"""
    return template
#initialise the llm model
def initialise_llm():
    llm = GoogleGenerativeAI(model = 'gemini-pro')
    return llm
 #generate the answer
def generate_text(user_input:str, template = hard_template(), llm = initialise_llm(), Docstore = initialize_document_store()):
    try:
        prompt = PromptTemplate.from_template(template)
        combine_docs_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(Docstore, combine_docs_chain)
        response = retrieval_chain.invoke({"input": user_input})
        print(response['answer'])
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()