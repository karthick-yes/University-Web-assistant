import pandas as pd
from dotenv import load_dotenv
from langchain import HuggingFaceHub
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
import qdrant_client
from httpx import Timeout
import os
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from langchain.chains import RetrievalQA
import argparse

load_dotenv()

MAX_LEN = 100
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', "-i", type=str, required=True)
    parser.add_argument('--template', '-t', type=str, required=False)
    args = parser.parse_args()
    user_input = args.input
    user_template = args.template
    if validate_input_length(user_input):

        generate_text(user_input, user_template)
        print(f"User input: {user_input}")
    else:
        raise ValueError(f"The input is longer than the expected limt {MAX_LEN}")


def initialize_embeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Initialize the embedding model."""
    return HuggingFaceEmbeddings(model_name=model_name)

def initialize_qdrant_client():
    """Initialize the Qdrant client."""
    return qdrant_client.QdrantClient(
        url=os.getenv('QDRANT_HOST'),
        api_key=os.getenv('QDRANT_API_KEY'),
        timeout=Timeout(timeout=None)
    )

def initialize_document_store(client, embeddings, collection_name="first"):
    """Initialize the document store."""
    return Qdrant(client=client, collection_name=collection_name, embeddings=embeddings)

def initialize_tools(helper, search):
    """Initialize the tools."""
    return [
        Tool(
            name="Ashoka_dataqa",
            func=helper.run,
            description='This function should  only be called whenever there is a question about the past events in ashoka, or those events that are supposed to be like what is mentioned in the database for a while.Some examples could be questions about courses, faculties etc.'
        ),
        Tool(
            name ="search",
            func=search.run,
            description="This tool must only be used if the context obtained from vectorstore is not enough to answer the question . useful for when you need to answer questions about upcoming and real time events/informations about ashoka university."
        )
    ]

def initialize_agent_executor(agent, tools):
    """Initialize the agent executor."""
    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

def validate_input_length(user_prompt: str) -> bool:
    return len(user_prompt) <= MAX_LEN

def generate_text(user_prompt:str, user_template:str=None, template_name:str=None):
    TEMPLATES = {
        "template1":"blah",
        "template2":"blahblah"
    }
    embeddings = initialize_embeddings()
    client = initialize_qdrant_client()
    doc_store = initialize_document_store(client, embeddings)
    llm = HuggingFaceHub(repo_id='Open-Orca/OpenOrca-Platypus2-13B')
    helper = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=doc_store.as_retriever(),
    )
    search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
    tools = initialize_tools(helper, search)
    prefix = """Answer the following questions as best you can, but speak only if you have enough data. You have access to the following tools:"""
    if user_template:
        suffix = f"{user_template}\n\nQuestion: {{input}}\n{{agent_scratchpad}}"
    elif template_name in TEMPLATES:
        suffix = f"{TEMPLATES[template_name]}\n\nQuestion: {{input}}\n{{agent_scratchpad}}"
    else:  
        suffix = """Begin! Remember to not make up things, if you do not know the answer, say "I dont know"

    Question: {input}
    {agent_scratchpad}"""
     
    prompt = ZeroShotAgent.create_prompt(
        tools, prefix=prefix, suffix=suffix, input_variables=["input", "agent_scratchpad"]
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
    agent_executor = initialize_agent_executor(agent, tools)
    return agent_executor.run(user_prompt)

if __name__ == '__main__':
    main()