import json
from datetime import datetime

import streamlit as st


def datastore_snowflake(type="plan"):
    conn = st.connection("snowflake")
    if type == "plan":
        with open('memory/plan_history_cache.json', 'r') as f:
            plan_data = json.load(f)

        for item in plan_data:
            for timestamp, data in item.items():
                try:
                    history = data['history']
                    conn.query("""
                        INSERT INTO PLAN_HISTORY 
                        (timestamp, chat_store_key, user_content, assistant_content, class_name, tool_used)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, params=[
                        datetime.strptime(timestamp, '%Y-%m-%d,%H:%M:%S'),
                        history['chat_store_key'],
                        history['user_content'],
                        history['assistant_content'],
                        history['class_name'],
                        json.dumps(history['tool_used'])
                    ], ttl=600)

                except Exception as e:
                    continue
                    print("数据已成功插入到 Snowflake 数据库中。")

    if type == "code":
        with open('memory/code_history_cache.json', 'r') as f:
            code_data = json.load(f)

        for item in code_data:
            for timestamp, data in item.items():
                try:
                    history = data['history']
                    conn.query("""
                        INSERT INTO CODE_HISTORY 
                        (timestamp, codebase_info, chat_store_key, user_content, assistant_content, class_name, tool_used)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, params=[
                        datetime.strptime(timestamp, '%Y-%m-%d,%H:%M:%S'),
                        json.dumps(data['codebase_info']),
                        history['chat_store_key'],
                        history['user_content'],
                        history['assistant_content'],
                        history['class_name'],
                        json.dumps(history['tool_used'])
                    ], ttl=600)
                    
                except Exception as e:
                    continue
                    print("数据已成功插入到 Snowflake 数据库中。")
