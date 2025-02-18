import google.generativeai as genai
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
import argparse
from typing import List, Any

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
MAX_LEN = 300

class GenerateAnswer:
    def __init__(self, ai_model: str, embedding_model: str, client: Any, collection_name: str):
        self.model = ai_model
        self.embedding_model = embedding_model
        self.client = client
        self.collection_name = collection_name

    def embedQuery(self, query: str) -> List[float]:
        """Embed the given query."""
        try:
            embeddedQuery = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="retrieval_query",
            )
            return embeddedQuery['embedding']
        except Exception as e:
            print(f"Error in embedding query: {e}")
            return []

    def similaritySearch(self, query: str, score_threshold: float, limit: int = 10) -> List[str]:
        """Perform similarity search based on the embedded query."""
        try:
            embedded_query = self.embedQuery(query)
            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=embedded_query,
                limit=limit,
                score_threshold=score_threshold,
            )
            page_contents = [hit.payload['text'] for hit in hits if hit.payload and 'text' in hit.payload]
            return page_contents
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []

    def promptTemplate(self, query: str) -> str:
        """Generate a prompt template with context."""
        context_list = self.similaritySearch(query, score_threshold=0.3)
        context = "\n".join(context_list)
        template = f"""
        You are a helpful AI assistant for university students.
        Answer based on the context provided.
        Context: {context}
        Input: {query}
        Answer:
        """
        return template

    def cookAnswer(self, query: str) -> str:
        """Generate an answer based on the query."""
        try:
            model = genai.GenerativeModel(self.model)
            result = model.generate_content(self.promptTemplate(query))
            return result.text
        except Exception as e:
            print(f"Error in generating answer: {e}")
            return "Sorry, I couldn't generate an answer at this time."

def initialize_qdrant_client():
    """Initialize the qdrant client."""
    return QdrantClient(
        url=os.getenv('QDRANT_HOST'),
        api_key=os.getenv('QDRANT_API_KEY'),
    )

def validate_input_length(user_input: str) -> bool:
    return len(user_input) <= MAX_LEN

def generate_answer(query: str) -> str:
    try:
        if not validate_input_length(query):
            raise ValueError(f'The input is longer than the {MAX_LEN} character limit')

        answer_generator = GenerateAnswer(
            ai_model="models/gemini-1.5-flash",
            embedding_model="models/embedding-001",
            client=initialize_qdrant_client(),
            collection_name="University_assistant"
        )

        return answer_generator.cookAnswer(query)

    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Generate an answer to a university-related query.")
    parser.add_argument('query', type=str, help="The query string to process")
    args = parser.parse_args()

    answer = generate_answer(args.query)
    print(f'User Query: {args.query}')
    print(f'Answer: {answer}')

if __name__ == "__main__":
    main()