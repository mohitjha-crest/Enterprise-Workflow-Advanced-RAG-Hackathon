from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.vector_stores.weaviate import WeaviateVectorStore

from dotenv import load_dotenv
load_dotenv()

import os
import weaviate

def completion_to_prompt(completion: str) -> str:
  return f"<s>[INST] {completion} [/INST] </s>\n"

def mistral_response(query):
    service_context = ServiceContext.from_defaults(
        llm = TogetherLLM(
            "mistralai/Mistral-7B-Instruct-v0.2",
            temperature = 0.8,
            max_tokens=256,
            top_p = 0.7,
            top_k = 50,
            is_chat_model = False,
            completion_to_prompt = completion_to_prompt
        ),
        embed_model = TogetherEmbedding("togethercomputer/m2-bert-80M-8k-retrieval")
    )

    client = weaviate.Client(
        os.environ['WEAVIATE_HOST'],
    )
    vector_store = WeaviateVectorStore(
        weaviate_client = client,
    )
    
    base_index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context = service_context)
    cohere_rerank = CohereRerank()

    memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
    reranking_chat_engine = base_index.as_chat_engine(
                memory = memory,
                node_postprocessors = [cohere_rerank]
    )

    response = reranking_chat_engine.query(query)
    return response
