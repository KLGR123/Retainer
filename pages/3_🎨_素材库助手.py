import os
import streamlit as st
from modules.pipelines import ImgGenPipeline
from modules.utils import *


def show_art_agent():
    if "img_pipeline" not in st.session_state:
        st.session_state.img_pipeline = ImgGenPipeline(openai_api_key=st.secrets["openai_api_key"])

    st.set_page_config(page_title="Retainer 游戏开发智能助手", page_icon="🎮")
    st.markdown("#### 你的美术素材 🎨")

    message_placeholder = st.empty()

    image_files = [f for f in os.listdir("assets/images") if f.endswith((".png", ".jpg", ".jpeg"))]
    if image_files:
        cols = st.columns(3)
        for idx, image_file in enumerate(image_files):
            with cols[idx % 3]:
                image_path = os.path.join("assets/images", image_file)
                st.image(image_path, use_column_width=True)
                st.caption(image_file)
    else:
        message_placeholder.success("暂无图片素材，请生成新的图片。")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if prompt := st.chat_input("描述你想要的美术效果 🎨"):
        with st.spinner(" Running..."):
            response = st.session_state.img_pipeline.step(prompt)
        
        for token in response:
            full_response = token
            message_placeholder.markdown("正在生成 "+full_response)

        st.session_state.img_pipeline.img_memory.save("memory/img_gen.json")
        st.rerun()

    script_path = os.path.join("assets/scripts", "所需素材.txt")
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
        st.sidebar.markdown("#### 所需素材")
        st.sidebar.code(script_content, language="text")

    if st.sidebar.button("🔁 初始生成"):
        for file in os.listdir("assets/images"):
            if file.endswith((".png", ".jpg", ".jpeg")):
                os.remove(os.path.join("assets/images", file))
        
        with st.spinner("Running..."):
            response = st.session_state.img_pipeline.step("请开始生成。")
        
        for token in response:
            full_response = token
            st.success("正在生成 "+full_response)

        st.session_state.img_pipeline.img_memory.save("memory/img_gen.json")

        st.rerun()


if __name__ == "__main__":
    show_art_agent()