import os
import json
import streamlit as st


if not os.path.exists("assets"):
    os.makedirs("assets")

if not os.path.exists("assets/codebase"):
    os.makedirs("assets/codebase")

if not os.path.exists("assets/codebase_commit"):
    os.makedirs("assets/codebase_commit")

if not os.path.exists("assets/scripts"):
    os.makedirs("assets/scripts")

if not os.path.exists("assets/images"):
    os.makedirs("assets/images")

if not os.path.exists("memory"):
    os.makedirs("memory")

if not os.path.exists("memory/plan.json"):
    with open("memory/plan.json", "w") as f:
        f.write("{}")

if not os.path.exists("memory/code.json"):
    with open("memory/code.json", "w") as f:
        f.write("{}")

if not os.path.exists("memory/img_gen.json"):
    with open("memory/img_gen.json", "w") as f:
        f.write("{}")

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("## 🕹️ Retainer Bot")
st.sidebar.success("选择你的策划 / 编程助手。")

if st.sidebar.button("🔄 重新开始"):
    folders_to_clear = ["assets/codebase", "assets/codebase_commit", "assets/images", "assets/scripts"]
    for folder in folders_to_clear:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            os.remove(file_path)

    memory_folder = "memory"
    for file in os.listdir(memory_folder):
        file_path = os.path.join(memory_folder, file)
        os.remove(file_path)

    for folder in folders_to_clear:
        if not os.path.exists(folder):
            os.makedirs(folder)

    if not os.path.exists("memory/plan.json"):
        with open("memory/plan.json", "w") as f:
            f.write("{}")

    if not os.path.exists("memory/code.json"):
        with open("memory/code.json", "w") as f:
            f.write("{}")

    if not os.path.exists("memory/img_gen.json"):
        with open("memory/img_gen.json", "w") as f:
            f.write("{}")

    with open("assets/plan.json", "w") as f:
        plan_structure = {
            "游戏策划": {
                "游戏玩法": "",
                "所需素材": {},
                "所需代码": {}
            }
        }
        f.write(json.dumps(plan_structure, ensure_ascii=False, indent=4))

    st.sidebar.success("已重新开始！")
    st.rerun()

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
    - 在敲定策划后，点击 ✅ 按钮，生成素材对应的 JSON 搭建文件。
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