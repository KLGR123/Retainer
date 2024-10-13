import os
import json
import shutil
import streamlit as st
from difflib import unified_diff

from modules.agents import PlanAgent, CodeAgent


def tool_called_callback(tool_name):
    st.session_state.tool_name = tool_name


def show_code_agent():
    code_agent = CodeAgent()
    code_agent.set_tool_called_callback(tool_called_callback)

    with open("modules/prompts/code_insight.md", "r", encoding="utf-8") as f:
        insight_prompt = f.read()

    st.set_page_config(page_title="Retainer 游戏开发智能助手", page_icon="🎮")
    # st.title("Retainer 代码库智能体 💻")

    st.markdown(
        """
        <style>
        .stApp {{
            background-image: url("https://unsplash.com/photos/two-red-and-white-dices-a6N685qLsHQ");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("你的代码库 📂")

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
            if st.button("⬆️"):
                for file in new_files.union(modified_files):
                    src = os.path.join("assets/codebase_commit", file)
                    dst = os.path.join("assets/codebase", file)
                    shutil.copy2(src, dst)

                for file in os.listdir("assets/codebase_commit"):
                    file_path = os.path.join("assets/codebase_commit", file)
                    os.remove(file_path)

                st.success("更新完成!")
                st.rerun()
        
        with col2:
            if st.button("🗑️"):
                # TODO: 将 agent memory 同步更新，告知 agent 代码没有被改动，而是废除了
                if selected_file:
                    commit_path = os.path.join("assets/codebase_commit", selected_file)
                    if os.path.exists(commit_path):
                        os.remove(commit_path)
                        st.success(f"{selected_file} 已废除!")
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
                response = code_agent.stream_chat(prompt)
                response_gen = response.response_gen
                
            for token in response_gen:
                full_response += token
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        current_history = code_agent.get_current_history(chat_store_persist_path="./memory/code_chat_store.json")
        code_agent.save_current_history_to_memory(current_history)
        code_agent.save_current_history_to_json(current_history, filename='./memory/code_history_cache.json')
        code_agent.tool_list = []

        st.rerun()

    if st.sidebar.button("🪄"):
        prompt = insight_prompt
        
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.spinner(f" Running..."):
                response = code_agent.stream_chat(prompt)
                response_gen = response.response_gen

            for token in response_gen:
                full_response += token
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        current_history = code_agent.get_current_history(chat_store_persist_path="./memory/code_chat_store.json")
        code_agent.save_current_history_to_memory(current_history)
        code_agent.save_current_history_to_json(current_history, filename='./memory/code_history_cache.json')
        code_agent.tool_list = []

        st.rerun()


def show_plan_agent():
    plan_agent = PlanAgent()
    plan_agent.set_tool_called_callback(tool_called_callback)

    st.set_page_config(page_title="Retainer 游戏开发智能助手", page_icon="🎮")
    # st.title("Retainer 策划智能体 📝")

    st.markdown(
        """
        <style>
        .stApp {{
            background-image: url("https://unsplash.com/photos/two-red-and-white-dices-a6N685qLsHQ");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.title("你的游戏策划 📝")

    script_files = [f for f in os.listdir("assets/scripts") if f.endswith(".json")]
    selected_file = st.sidebar.selectbox("选择一个文件查看内容", script_files)

    if selected_file:
        with open(os.path.join("assets/scripts", selected_file), "r", encoding="utf-8") as f:
            file_content = json.load(f)
        st.sidebar.markdown(f"#### {selected_file[:-5]}")
        st.sidebar.code(json.dumps(file_content, indent=4, ensure_ascii=False), language="json")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "🥸" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("畅谈任何关于游戏的想法 💡"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="🥸"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            full_response = ""

            with st.spinner(f" Running..."):
                response = plan_agent.stream_chat(prompt)
                response_gen = response.response_gen

            for token in response_gen:
                full_response += token
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
                        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        current_history = plan_agent.get_current_history(chat_store_persist_path="./memory/plan_chat_store.json")
        plan_agent.save_current_history_to_memory(current_history)
        plan_agent.save_current_history_to_json(current_history, filename='./memory/plan_history_cache.json')
        plan_agent.tool_list = []

        st.rerun()


if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "code":
        show_code_agent()

    if len(sys.argv) > 1 and sys.argv[1] == "plan":
        show_plan_agent()
