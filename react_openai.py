# -*- coding: utf-8 -*-

import os
import time
import openai
openai.api_key = "sk-proj-A8ilUbtyMXhfLsGzKi9aT3BlbkFJAIWL77g2B1sMv7hwoyXf"

from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.core.tools import QueryEngineTool
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import SimpleDirectoryReader, Settings

Settings.llm = OpenAI(model="gpt-4", temperature=0.1)

base_prompt = """\
你是一个专业的辅助用户实现 Unity 游戏开发的智能体。
作为游戏开发智能体，你应当礼貌地拒绝任何与游戏开发无关的交流。
你的用户通常是一些初学者，他们希望使用 Unity 进行游戏开发，但是对 Unity 的使用并不熟悉。

如下是一些值得参考的经验：
(0) 在最开始时，你最好先使用 read_entire_codebase 了解一下目前代码库的结构和内容。如果为空则说明用户想创建一个新游戏；
(1) 用户通常会在最开始描述自己关于构建新游戏的抽象想法，你需要以一个专业的游戏设计策划师的角度，\
    将该游戏具体玩法、场景搭建需求等等按照步骤详细地描述出来；
(2) 你需要生成 n 个 .cs 文件来实现该游戏。你需要给每个 .cs 文件起名，输出每个 .cs 文件里面的代码，\
    带有明确的注释；你应该像一个 c# 专家一样生成简洁易懂的代码，同时务必满足需求中的每一点；
(3) 调用合适的工具 write_code_to_file 将代码文件写入代码库；
(4) 用户在之后的交互中会对当前游戏提出一些修改想法，你需要充分理解用户的意图，\
    将该意图对应的可能存在的代码改动需求按步骤详细地描述出来；
(5) 之后，你应当调用合适的工具 read_code_from_file，根据需要读取当前时刻代码库中的某些代码文件的内容，\
    结合用户的改动意图增删改动代码文件中的具体代码，并调用工具 write_code_to_file 将新的完整代码写入代码文件，\
    以实现用户希望的改动想法；在你使用 write_code_to_file 工具写入新代码时，请务必确保你写入的代码是完整合理的，\
    并在交互后告知用户写入的代码和原代码的差异并对比；
(6) 与你的用户细致且积极的交流，说明你执行的操作等，并给出明确的反馈；\
    当你不确定用户的想法和需求时，你应当主动询问用户；
(7) 对于用户在询问某种游戏想法或设计在代码库的具体代码块位置时，\
    你可以调用 read_entire_codebase 或 query_codebase_content 来获取并进一步分析；
"""

insight_prompt = "我现在有点不知道下一步该做什么。请以游戏策划师的角度思考当前游戏的某个具体的玩法改进，并给出对应的建议和代码修改。"

def query_codebase_content(query: str, k: int) -> str:
    """根据 query 寻找当前时刻代码库中的最相关的 k 个代码片段。
    该工具用于根据语义相似度检索相关代码块，如果需要修改代码仍然需要使用 read_code_from_file 和 write_code_to_file 实现读写。"""

    documents = SimpleDirectoryReader("codebase").load_data()
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

    if not os.path.exists(os.path.join("codebase", file_name)):
        return f"{file_name} 文件不存在。"

    with open(os.path.join("codebase", file_name), "r", encoding="utf-8") as f:
        file_content = f.read()
    
    return f"{file_name} 文件中的代码是：\n```{file_content}```"

def read_entire_codebase() -> str:
    """读取整个 codebase 文件夹中的所有 .cs 文件内容，返回文件名和对应的代码内容。用于快速了解整个代码库的结构。"""
    
    codebase_content = ""
    for root, dirs, files in os.walk("codebase"):
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

    with open(os.path.join("codebase", file_name), "w") as f:
        f.write(code)

    return f"{file_name} 写入新代码完成。"

def delete_file_from_codebase(file_name: str) -> str:
    """删除文件 file_name 中的全部代码以及文件本身，file_name 应当以 .cs 结尾。"""

    if not file_name.endswith(".cs"):
        file_name += ".cs"

    if not os.path.exists(os.path.join("codebase", file_name)):
        return f"{file_name} 文件不存在。"

    os.remove(os.path.join("codebase", file_name))
    return f"{file_name} 删除完成。"

tools = [
    FunctionTool.from_defaults(fn=write_code_to_file),
    FunctionTool.from_defaults(fn=read_code_from_file),
    # FunctionTool.from_defaults(fn=query_codebase_content),
    FunctionTool.from_defaults(fn=read_entire_codebase),
    FunctionTool.from_defaults(fn=delete_file_from_codebase)
]

agent = ReActAgent.from_tools(
    tools,
    verbose=True,
    context=base_prompt,
)

if __name__ == "__main__":
    import streamlit as st

    st.set_page_config(page_title="Retainer 游戏开发智能助手 🎮", page_icon=":robot_face:")
    st.title("Retainer 游戏开发智能助手 🎮")
    
    st.sidebar.title("你的代码库 📂")

    code_files = [f for f in os.listdir("codebase") if f.endswith(".cs")]
    selected_file = st.sidebar.selectbox("选择一个文件查看内容", code_files)

    if selected_file:
        with open(os.path.join("codebase", selected_file), "r", encoding="utf-8") as f:
            file_content = f.read()
        st.sidebar.markdown(f"#### {selected_file}")
        st.sidebar.code(file_content, language="csharp")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("畅谈任何关于游戏的想法 💡"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            response = agent.stream_chat(prompt)
            print(agent.memory)
            response_gen = response.response_gen

            for token in response_gen:
                full_response += token
                message_placeholder.markdown(full_response + "▌")
                # time.sleep(0.01)
            
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

    if st.sidebar.button("✨"):
        prompt = insight_prompt
        # st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            response = agent.stream_chat(prompt)
            response_gen = response.response_gen

            for token in response_gen:
                full_response += token
                message_placeholder.markdown(full_response + "▌")
                # time.sleep(0.01)
            
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()