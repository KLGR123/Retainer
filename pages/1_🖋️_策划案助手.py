import os
import json
import streamlit as st

from modules.pipelines import PlanPipeline, SceneGenPipeline
from modules.utils import *


def split_plan_json():
    plan = load_json("assets/plan.json")
    
    gameplay = plan["游戏策划"]["游戏玩法"]
    write_file("assets/scripts/游戏玩法.txt", gameplay)
    
    assets = plan["游戏策划"]["所需素材"]
    assets_text = "\n".join([f"{k}: {v}" for k,v in assets.items()])
    write_file("assets/scripts/所需素材.txt", assets_text)
    
    code = plan["游戏策划"]["所需代码"] 
    code_text = "\n".join([f"{k}: {v}" for k,v in code.items()])
    write_file("assets/scripts/所需代码.txt", code_text)


def show_plan_agent():
    if "scene_gen_pipeline" not in st.session_state:
        st.session_state.scene_gen_pipeline = SceneGenPipeline(openai_api_key=st.secrets["openai_api_key"])

    if "plan_pipeline" not in st.session_state:
        st.session_state.plan_pipeline = PlanPipeline(openai_api_key=st.secrets["openai_api_key"])

    st.set_page_config(page_title="Retainer 游戏开发智能助手", page_icon="🎮")
    st.sidebar.title("你的游戏策划 📝")

    # if st.sidebar.button("⬆️"): # TODO
    #     from modules.datastore.datastore_snowflake import datastore_snowflake
    #     datastore_snowflake(type="plan")
    #     st.sidebar.success("数据存储已更新！")

    script_files = [f for f in os.listdir("assets/scripts") if f.endswith(".txt") or f.endswith(".json")]
    selected_file = st.sidebar.selectbox("选择一个文件查看内容", script_files)

    if selected_file:
        file_content = read_file(os.path.join("assets/scripts", selected_file))
        
        if selected_file.endswith(".txt"):
            st.sidebar.markdown(f"#### {selected_file[:-4]}")
            st.sidebar.code(file_content, language="text")
        elif selected_file.endswith(".json"):
            st.sidebar.markdown(f"#### {selected_file[:-5]}")
            st.sidebar.code(file_content, language="json")

    if st.sidebar.button("✅ 定稿存档"):
        st.session_state.scene_gen_pipeline.step()
        st.session_state.scene_gen_pipeline.scene_gen_memory.save("memory/scene_gen.json")
        st.sidebar.success("已存档！")


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
                response = st.session_state.plan_pipeline.step(prompt)

            for token in response:
                full_response += token
                message_placeholder.markdown(full_response + "▌")

            full_response = full_response if full_response else "已更新游戏策划。"
            message_placeholder.markdown(full_response)
                        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.plan_pipeline.plan_memory.save("memory/plan.json")

        if os.path.exists("assets/plan.json"):
            split_plan_json()

        st.rerun()


if __name__ == "__main__":
    show_plan_agent()