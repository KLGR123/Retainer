import os

from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import SimpleDirectoryReader
from llama_index.core import PromptTemplate

from ..vectorstore import CodebaseQueryEngine
from .scripts import read_scene_gameplay
from ..utils import read_config

import streamlit as st


codebase_query_engine = CodebaseQueryEngine(k=1)

def query_codebase_content(query: str) -> str:
    """根据 query 寻找当前时刻代码库中的最相关（语义相似度）的 1 个代码片段。
    该工具用于根据语义相似度检索相关代码块，如果需要修改代码仍然需要使用 read_code_from_file 和 write_code_to_file 实现读写。"""
    
    codebase_query_engine.update()
    response = codebase_query_engine.query(query)
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


def write_code_to_file(file_name: str, commit: str) -> str:
    """将 C# 代码 code 写入到文件 file_name 中，file_name 应当以 .cs 结尾，commit 应当是对该代码文件如何改动的详细具体的描述，即一句 commit message；
    如果 file_name 文件此时还不存在，则该工具自动创建文件并写入 code；如果 file_name 文件已经存在，该工具覆盖式写入。"""

    if not file_name.endswith(".cs"):
        file_name += ".cs"

    code = ""
    if os.path.exists(os.path.join("assets/codebase", file_name)):
        with open(os.path.join("assets/codebase", file_name), "r", encoding="utf-8") as f:
            code = f.read()

    config = read_config()
    llm_ = OpenAI(model=config.get("code_model"), 
        temperature=config.get("code_temperature"), 
        api_key=st.secrets["openai_api_key"]
    )

    content_ = read_scene_gameplay()

    template_ = (
        "你是一个 unity 游戏代码开发专家。给定用户当前代码修改的 commit 需求描述，你需要依据游戏的玩法描述和当前该文件的代码，像一个 c# 专家一样完成/修改它，以满足 commit 需求中的每一点；代码带有明确的注释；你被鼓励尽可能多生成代码；你不被允许留有一些待实现的函数或代码块。需要注意的是，你在写代码的时候如果要命名某个 class，那么该 class 的命名应当与当前文件名保持一致。\n\n"
        "用户的 commit 需求描述是：{commit}\n"
        "当前游戏的玩法描述是：{gameplay_content}\n"
        "当前`{file_name}`文件下的全部代码如下```\n{code}\n```\n"
        "你的输出是修改后的代码（保持完整性，不修改的地方直接复制），不要输出任何解释。请开始。"
    )

    qa_template = PromptTemplate(template_)
    messages = qa_template.format_messages(gameplay_content=content_, 
        code=code, 
        commit=commit, 
        file_name=file_name
    )

    resp = llm_.chat(messages)
    resp = str(resp)

    start_marker, end_marker = "```csharp", "```"
    start_index = resp.find(start_marker)
    end_index = resp.find(end_marker, start_index + len(start_marker)) if start_index != -1 else -1

    if start_index != -1 and end_index != -1:
        start_index += len(start_marker)
        new_code = resp[start_index:end_index].strip()
    else:
        new_code = resp.strip()

    with open(os.path.join("assets/codebase_commit", file_name), "w", encoding="utf-8") as f:
        f.write(new_code)

    return f"{file_name} 写入新代码完成。"


def delete_file_from_codebase(file_name: str) -> str:
    """删除文件 file_name 中的全部代码以及文件本身，file_name 应当以 .cs 结尾。除非用户明确要求删除文件，否则不要使用该工具。"""

    if not file_name.endswith(".cs"):
        file_name += ".cs"

    if not os.path.exists(os.path.join("assets/codebase", file_name)):
        return f"{file_name} 文件不存在。"

    os.remove(os.path.join("assets/codebase", file_name))
    return f"{file_name} 删除完成。"