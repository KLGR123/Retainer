# -*- coding: utf-8 -*-

import os
import time
import openai
openai.api_key = "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"

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

planning_prompt = """\
    ### 角色
    你是一个专业的辅助用户实现 Unity 游戏开发的游戏策划师。

    ### 背景
    作为游戏开发智能体，你应当礼貌地拒绝任何与游戏开发无关的交流。
    你的用户通常是一些初学者，他们希望使用 Unity 进行游戏开发，但是对 Unity 的使用并不熟悉。

    ### 输出要求
    你会帮助用户生成两个文件，一个是场景搭建.txt，一个是游戏玩法.txt。

    ### 案例
    - 用户输入:
    请你帮我设计一个小鸟飞行并躲避柱子的游戏。
    - 输出:
    - **1. 场景搭建.txt**
        1、放置小鸟图片，并在小鸟上加载小鸟控制代码
        2、放置柱子图片，并在柱子上加载柱子控制代码
        3、放置背景图片，并在背景上加载背景控制代码
        4、创建游戏控制空物体，并在游戏控制空物体上加载游戏控制代码
        5、创建UI，并加载UI控制代码
    - **2. 游戏玩法.txt**
    {
    "游戏描述": {
        "玩法": "玩家点击屏幕触发小鸟飞起，否则小鸟下落。场景中会有连续不断的上下两根柱子向小鸟移动，玩家需要控制小鸟通过两根柱子之间的空隙，否则游戏结束。",
        "所需素材": {
        "bird.png": "小鸟的图片",
        "pipe.png": "柱子的图片",
        "background.png": "背景的图片"
        },
        "所需代码": {
        "bird.cs": "用于控制小鸟移动的代码",
        "pipe_control.cs": "用于控制柱子移动的代码",
        "background_control.cs": "用于控制背景的代码",
        "ui_control.cs": "用于控制用户界面的代码",
        "game_control.cs": "用于管理整个游戏逻辑的代码"
        }
    }
    }
    - 场景搭建.txt
    1、放置小鸟图片，并在小鸟上加载小鸟控制代码
    2、放置柱子图片，并在柱子上加载柱子控制代码
    3、放置背景图片，并在背景上加载背景控制代码
    4、创建游戏控制空物体，并在游戏控制空物体上加载游戏控制代码
    5、创建UI，并加载UI控制代码
"""

def query_planning_content(query: str, k: int) -> str:
    """
    根据 query 寻找当前时刻计划文件夹中的最相关的 k 个计划片段。
    该工具用于根据语义相似度检索相关的计划块，如果需要修改计划仍然需要使用 read_plan_from_file 和 write_plan_to_file 实现读写。
    """

    documents = SimpleDirectoryReader("planning").load_data()
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

def read_plan_from_file(file_name: str) -> str:
    """读取当前文件 file_name 中的全部计划，file_name 应当以 .plan 结尾。"""

    if not file_name.endswith(".txt"):
        file_name += ".txt"

    if not os.path.exists(os.path.join("planning", file_name)):
        return f"{file_name} 文件不存在。"

    with open(os.path.join("planning", file_name), "r", encoding="utf-8") as f:
        file_content = f.read()
    
    return f"{file_name} 文件中的计划是：\n```{file_content}```"

def read_entire_planning() -> str:
    """读取整个 planning 文件夹中的所有 .plan 文件内容，返回文件名和对应的计划内容。用于快速了解整个计划库的结构。"""
    
    planning_content = ""
    for root, dirs, files in os.walk("planning"):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                planning_content += f"在 {file} 文件中的计划是：\n```\n{file_content}\n```\n\n"
    
    return planning_content if planning_content else "planning 中没有找到 .txt 文件。"

def write_plan_to_file(file_name: str, plan: str) -> str:
    """将计划写入到文件 file_name 中，file_name 应当以 .txt 结尾。
    如果 file_name 文件此时还不存在，则该工具自动创建文件并写入 planning；如果 file_name 文件已经存在，该工具覆盖式写入 planning。"""

    if not file_name.endswith(".txt"):
        file_name += ".txt"

    with open(os.path.join("planning", file_name), "w") as f:
        f.write(plan)

    return f"{file_name} 写入新计划完成。"

def delete_plan_from_planning(file_name: str) -> str:
    """删除文件 file_name 中的全部计划以及文件本身，file_name 应当以 .txt 结尾。"""

    if not file_name.endswith(".txt"):
        file_name += ".txt"

    if not os.path.exists(os.path.join("planning", file_name)):
        return f"{file_name} 文件不存在。"

    os.remove(os.path.join("planning", file_name))
    return f"{file_name} 删除完成。"

planning_tools = [
    FunctionTool.from_defaults(fn=query_planning_content),
    FunctionTool.from_defaults(fn=write_plan_to_file),
    # FunctionTool.from_defaults(fn=query_codebase_content),
    FunctionTool.from_defaults(fn=read_entire_planning),
    FunctionTool.from_defaults(fn=delete_plan_from_planning)
]

planning_agent = ReActAgent.from_tools(
    planning_tools,
    verbose=True,
    context=planning_prompt,
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
        avatar = "🤓" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("畅谈任何关于游戏的想法 💡"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="🤓"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            full_response = ""

            with st.spinner(" Thinking..."):
                response = planning_agent.stream_chat(prompt)
                print(planning_agent.memory)
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

        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            full_response = ""

            with st.spinner(" Thinking..."):
                response = planning_agent.stream_chat(prompt)
                response_gen = response.response_gen

            for token in response_gen:
                full_response += token
                message_placeholder.markdown(full_response + "▌")
                # time.sleep(0.01)
            
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()