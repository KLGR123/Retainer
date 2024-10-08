import os
import json


def write_gameplay_script(content: dict) -> str:
    """将游戏策划写入到指定的 .json 文件中，content 是游戏玩法的内容，为一个字典；
    如果文件此时还不存在，则该工具自动创建文件并写入游戏策划；如果文件已经存在，该工具覆盖式写入策划案。"""

    file_path = os.path.join("assets/scripts", "游戏策划.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

    return f"游戏策划写入完成。"


def write_scene_script(content: list[str]) -> str:
    """将场景搭建写入到指定的 .json 文件中，content 是场景搭建的步骤，为一个列表，其元素是字符串；
    如果文件此时还不存在，则该工具自动创建文件并写入场景搭建；如果文件已经存在，该工具覆盖式写入场景搭建说明。"""

    file_path = os.path.join("assets/scripts", "场景搭建.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

    return f"场景搭建写入完成。"


def read_entire_planning() -> str:
    """读取整个 scripts 文件夹中的所有策划文件内容，返回文件名和对应的内容。
    用于快速了解现阶段用户对游戏策划和场景搭建的策划。"""
    
    planning_content = ""
    scene_file_path = os.path.join("assets/scripts", "场景搭建.json")
    gameplay_file_path = os.path.join("assets/scripts", "游戏策划.json")

    if os.path.exists(scene_file_path):
        with open(scene_file_path, "r", encoding="utf-8") as f:
            scene_content = json.load(f)
        planning_content += f"在 场景搭建.json 文件中的内容是：\n```\n{json.dumps(scene_content, ensure_ascii=False, indent=4)}\n```\n\n"

    if os.path.exists(gameplay_file_path):
        with open(gameplay_file_path, "r", encoding="utf-8") as f:
            gameplay_content = json.load(f)
        planning_content += f"在 游戏策划.json 文件中的内容是：\n```\n{json.dumps(gameplay_content, ensure_ascii=False, indent=4)}\n```\n\n"
    
    return planning_content if planning_content else "scripts 中没有找到 .json 文件。"

