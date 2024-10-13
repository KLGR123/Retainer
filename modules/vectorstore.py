from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import SimpleDirectoryReader

from .utils import read_config

import streamlit as st


class CodebaseQueryEngine:
    def __init__(self, k: int = 1):
        self.k = k

        config = read_config()
        Settings.llm = OpenAI(model=config.get("codebase_model"), 
            temperature=config.get("code_temperature"), 
            api_key=st.secrets["openai_api_key"]
        )
        Settings.embed_model = OpenAIEmbedding()

    def update(self):
        try:
            documents_ = SimpleDirectoryReader("assets/codebase").load_data()
            self.index = VectorStoreIndex.from_documents(documents_)
            self.CodebaseRetriever = VectorIndexRetriever(
                index=self.index,
                similarity_top_k=self.k,
            )

            response_synthesizer = get_response_synthesizer()
            self.query_engine = RetrieverQueryEngine(
                retriever=self.CodebaseRetriever,
                response_synthesizer=response_synthesizer,
                node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.75)],
            )
        
        except FileNotFoundError:
            print("错误: assets/codebase 目录不存在。")
        except Exception as e:
            print(f"更新索引时发生错误: {str(e)}")

    def query(self, query: str) -> str:
        try:
            return self.query_engine.query(query)

        except Exception as e:
            print(f"查询时发生错误: {str(e)}")
            return ""