import os

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import SimpleDirectoryReader


def query_codebase_content(query: str, k: int) -> str:
    """根据 query 寻找当前时刻代码库中的最相关的 k 个代码片段。
    该工具用于根据语义相似度检索相关代码块，如果需要修改代码仍然需要使用 read_code_from_file 和 write_code_to_file 实现读写。"""

    documents = SimpleDirectoryReader("assets/codebase").load_data()
    index = VectorStoreIndex.from_documents(documents)
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=k,
    )

    response_synthesizer = get_response_synthesizer()
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.75)],
    )

    response = query_engine.query(query)
    return response


def read_code_from_file(file_name: str) -> str:
    """读取当前文件 file_name 中的全部 C# 代码，file_name 应当以 .cs 结尾。"""

    if not file_name.endswith(".cs"):
        file_name += ".cs"

    if not os.path.exists(os.path.join("assets/codebase", file_name)):
        return f"{file_name} 文件不存在。"

    with open(os.path.join("assets/codebase", file_name), "r", encoding="utf-8") as f:
        file_content = f.read()
    
    return f"{file_name} 文件中的代码是：\n```{file_content}```"


def read_entire_codebase() -> str:
    """读取整个 codebase 文件夹中的所有 .cs 文件内容，返回文件名和对应的代码内容。用于快速了解整个代码库的结构。"""
    
    codebase_content = ""
    for root, dirs, files in os.walk("assets/codebase"):
        for file in files:
            if file.endswith(".cs"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                codebase_content += f"在 {file} 文件中的代码是：\n```\n{file_content}\n```\n\n"
    
    return codebase_content if codebase_content else "codebase 中没有找到 .cs 文件。"


def write_code_to_file(file_name: str, code: str) -> str:
    """将 C# 代码 code 写入到文件 file_name 中，file_name 应当以 .cs 结尾。
    如果 file_name 文件此时还不存在，则该工具自动创建文件并写入 code；如果 file_name 文件已经存在，该工具覆盖式写入 code。"""

    if not file_name.endswith(".cs"):
        file_name += ".cs"

    with open(os.path.join("assets/codebase", file_name), "w") as f:
        f.write(code)

    return f"{file_name} 写入新代码完成。"


def delete_file_from_codebase(file_name: str) -> str:
    """删除文件 file_name 中的全部代码以及文件本身，file_name 应当以 .cs 结尾。"""

    if not file_name.endswith(".cs"):
        file_name += ".cs"

    if not os.path.exists(os.path.join("assets/codebase", file_name)):
        return f"{file_name} 文件不存在。"

    os.remove(os.path.join("assets/codebase", file_name))
    return f"{file_name} 删除完成。"