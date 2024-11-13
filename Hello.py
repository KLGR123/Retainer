import os
import streamlit as st


if not os.path.exists("assets"):
    os.makedirs("assets")

if not os.path.exists("assets/codebase"):
    os.makedirs("assets/codebase")

if not os.path.exists("assets/codebase_commit"):
    os.makedirs("assets/codebase_commit")

if not os.path.exists("assets/scripts"):
    os.makedirs("assets/scripts")

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("## 🕹️ Retainer Bot")
st.sidebar.success("选择你的策划 / 编程助手。")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    *Retainer 是一个游戏开发助手，可以帮助你完成游戏策划和开发工作。*

    *免责声明：该助手仍在开发中，其功能会不断更新。目前仍不完善，请谨慎使用。*

    **👈 选择一个助手** 来查看他们的功能。
    """
)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """

    ###### 📌 如何使用它们

    - 在助手对话框中输入你的需求。
    - 对于`策划案助手` 🤖，你会得到和游戏设计策划案。
    - 对于`代码库助手` 🤖，你会得到若干代码文件。
    - 你可以在 `commit` 文件夹中找到新生成的文件并对比差异。
    - 如果满意，你可以点击 ✅ 将这些文件保存到你的代码库中，否则点击 🗑️ 放弃这些文件。
    - 🪄 获取灵感 可以在你没有想法的时候给予一些改进灵感。
    """
)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    ###### 📌 帮助我们变得更好

    - 在结束时点击 ⬆️ 将你的对话历史上传到我们的数据库中。
    - 尝试尽可能多的对话格式或描述，这样可以帮助我们更好地理解开发者的需求。
    """
)