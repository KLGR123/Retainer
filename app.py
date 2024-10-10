import os
import json
import streamlit as st
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
    st.sidebar.title("你的代码库 📂")
    code_files = [f for f in os.listdir("assets/codebase") if f.endswith(".cs")]
    selected_file = st.sidebar.selectbox("选择一个文件查看内容", code_files)

    if selected_file:
        with open(os.path.join("assets/codebase", selected_file), "r", encoding="utf-8") as f:
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

            with st.spinner(f" Running..."):
                response = code_agent.stream_chat(prompt)
                response_gen = response.response_gen
                
            for token in response_gen:
                full_response += token
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

    if st.sidebar.button("✨"):
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
        st.rerun()


def show_plan_agent():
    plan_agent = PlanAgent()
    plan_agent.set_tool_called_callback(tool_called_callback)

    st.set_page_config(page_title="Retainer 游戏开发智能助手", page_icon="🎮")
    # st.title("Retainer 策划智能体 📝")
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
                response = plan_agent.stream_chat(prompt)
                response_gen = response.response_gen

            for token in response_gen:
                full_response += token
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
                        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()


if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "code":
        show_code_agent()

    if len(sys.argv) > 1 and sys.argv[1] == "plan":
        show_plan_agent()
