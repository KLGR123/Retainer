import os
import json
import shutil
import streamlit as st
from difflib import unified_diff

from modules.pipelines import CodePipeline
from modules.utils import *


def split_code_json() -> None:
    code_data = load_json("assets/code_buffer.json")
    for filename, code in code_data.items():
        with open(os.path.join("assets/codebase_commit", filename), "w", encoding="utf-8") as f:
            f.write(code)


def show_code_agent():
    if "code_pipeline" not in st.session_state:
        st.session_state.code_pipeline = CodePipeline(openai_api_key=st.secrets["openai_api_key"])

    st.set_page_config(page_title="Retainer 游戏开发智能助手", page_icon="🎮")
    st.sidebar.title("你的代码库 📂")

    # if st.sidebar.button("⬆️"): # TODO
    #     from modules.datastore.datastore_snowflake import datastore_snowflake
    #     datastore_snowflake(type="code")
    #     st.sidebar.success("数据存储已更新！")

    code_files = [f for f in os.listdir("assets/codebase") if f.endswith(".cs")]
    selected_file = st.sidebar.selectbox("选择一个文件查看内容", code_files)

    if selected_file:
        with open(os.path.join("assets/codebase", selected_file), "r", encoding="utf-8") as f:
            file_content = f.read()
        st.sidebar.markdown(f"#### {selected_file}")
        st.sidebar.code(file_content, language="csharp")

    codebase_files = set(f for f in os.listdir("assets/codebase") if f.endswith(".cs"))
    commit_files = set(f for f in os.listdir("assets/codebase_commit") if f.endswith(".cs"))

    new_files = commit_files - codebase_files
    modified_files = set()

    for file in commit_files.intersection(codebase_files):
        codebase_path = os.path.join("assets/codebase", file)
        commit_path = os.path.join("assets/codebase_commit", file)
        
        with open(codebase_path, "r", encoding="utf-8") as f1, open(commit_path, "r", encoding="utf-8") as f2:
            if f1.read() != f2.read():
                modified_files.add(file)
    
    with st.sidebar.expander("`commit`"):
        def generate_diff(old_content, new_content):
            diff = unified_diff(
                old_content.splitlines(), 
                new_content.splitlines(), 
                fromfile='当前版本', 
                tofile='提交版本', 
                lineterm=''
            )
            return '\n'.join(diff)

        all_files = list(new_files.union(modified_files))
        selected_file = st.selectbox(" ", all_files)

        if selected_file:
            codebase_path = os.path.join("assets/codebase", selected_file)
            commit_path = os.path.join("assets/codebase_commit", selected_file)
            
            if os.path.exists(codebase_path) and os.path.exists(commit_path):
                with open(codebase_path, "r", encoding="utf-8") as f:
                    codebase_content = f.read()
                with open(commit_path, "r", encoding="utf-8") as f:
                    commit_content = f.read()
                
                diff_content = generate_diff(codebase_content, commit_content)
                st.markdown(f"##### *{selected_file} （改动文件）*")
                st.code(diff_content, language="diff")

            elif os.path.exists(commit_path):
                with open(commit_path, "r", encoding="utf-8") as f:
                    commit_content = f.read()
                st.markdown(f"##### *{selected_file} (新文件)*")
                st.code(commit_content, language="csharp")

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅"):
                for file in new_files.union(modified_files):
                    src = os.path.join("assets/codebase_commit", file)
                    dst = os.path.join("assets/codebase", file)
                    shutil.copy2(src, dst)

                for file in os.listdir("assets/codebase_commit"):
                    file_path = os.path.join("assets/codebase_commit", file)
                    os.remove(file_path)

                code = load_json("assets/code_buffer.json")
                dump_json("assets/code_memo.json", code)
                dump_json("assets/code_buffer.json", code)

                st.success("更新完成!")
                st.rerun()
        
        with col2:
            if st.button("🗑️"):
                for file in os.listdir("assets/codebase_commit"):
                    file_path = os.path.join("assets/codebase_commit", file)
                    os.remove(file_path)

                dump_json("assets/code_buffer.json", load_json("assets/code_memo.json"))

                st.session_state.code_pipeline.pop_step()
                st.session_state.code_pipeline.code_memory.save("memory/code.json")
                st.success("待提交代码已废除!")
                st.rerun()

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

            with st.spinner(f" Running..."):
                response = st.session_state.code_pipeline.step(prompt)
                
            for token in response:
                full_response += token
                message_placeholder.markdown(full_response + "▌")

            full_response = full_response if full_response else "已更新代码素材。"
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.code_pipeline.code_memory.save("memory/code.json")

        if os.path.exists("assets/code_buffer.json"):
            split_code_json()

        st.rerun()

    # if st.sidebar.button("🪄 获取灵感"):
    #     with st.chat_message("assistant", avatar="🤖"):
    #         message_placeholder = st.empty()
    #         full_response = ""
            
    #         with st.spinner(f" Running..."):
    #             response = st.session_state.code_pipeline.insight_step()

    #         for token in response:
    #             full_response += token
    #             message_placeholder.markdown(full_response + "▌")

    #         message_placeholder.markdown(full_response)

    #     st.session_state.messages.append({"role": "assistant", "content": full_response})
    #     st.session_state.code_pipeline.code_memory.save("memory/code.json")

    #     if os.path.exists("assets/code_buffer.json"):
    #         split_code_json()

    #     st.rerun()
    
    if st.sidebar.button("🔁 初始生成"):
        for file in os.listdir("assets/codebase"):
            if file.endswith(".cs"):
                os.remove(os.path.join("assets/codebase", file))

        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.spinner(f" Running..."):
                response = st.session_state.code_pipeline.init_step()

            for token in response:
                full_response = token
                message_placeholder.success("正在生成 "+full_response)

            full_response = "已更新代码素材。"
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.code_pipeline.code_memory.save("memory/code.json")

        if os.path.exists(f"assets/code_buffer.json"):
            split_code_json()

        st.rerun()


if __name__ == "__main__":
    show_code_agent()