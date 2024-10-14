import json
from datetime import datetime

import streamlit as st


def datastore(type="plan"):
    conn = st.connection('mysql', type='sql')

    if type == "plan":
        with open('memory/plan_history_cache.json', 'r') as f:
            plan_data = json.load(f)

        for item in plan_data:
            for timestamp, data in item.items():
                history = data['history']
                conn.query("""
                    INSERT INTO plan_history 
                    (timestamp, chat_store_key, user_content, assistant_content, class_name, tool_used)
                    VALUES (:timestamp, :chat_store_key, :user_content, :assistant_content, :class_name, :tool_used)
                """, params={
                    "timestamp": datetime.strptime(timestamp, '%Y-%m-%d,%H:%M:%S'),
                    "chat_store_key": history['chat_store_key'],
                    "user_content": history['user_content'],
                    "assistant_content": history['assistant_content'],
                    "class_name": history['class_name'],
                    "tool_used": json.dumps(history['tool_used'])
                }, ttl=600)

    if type == "code":
        with open('memory/code_history_cache.json', 'r') as f:
            code_data = json.load(f)

        for item in code_data:
            for timestamp, data in item.items():
                history = data['history']
                conn.query("""
                    INSERT INTO code_history 
                    (timestamp, codebase_info, chat_store_key, user_content, assistant_content, class_name, tool_used)
                    VALUES (:timestamp, :codebase_info, :chat_store_key, :user_content, :assistant_content, :class_name, :tool_used)
                """, params={
                    "timestamp": datetime.strptime(timestamp, '%Y-%m-%d,%H:%M:%S'),
                    "codebase_info": json.dumps(data['codebase_info']),
                    "chat_store_key": history['chat_store_key'],
                    "user_content": history['user_content'],
                    "assistant_content": history['assistant_content'],
                    "class_name": history['class_name'],
                    "tool_used": json.dumps(history['tool_used'])
                }, ttl=600)

    print("数据已成功插入到MySQL数据库中。")