from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import os
from modules.pipelines import PlanPipeline, CodePipeline

app = Flask(__name__)
socketio = SocketIO(app)
OUTPUT_DIR = "output"

def create_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    empty_index_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(empty_index_path, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n</body>\n</html>')

create_output_dir()
plan_pipeline = PlanPipeline()
code_pipeline = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory('output', filename)

@socketio.on('user_message')
def handle_message(message):
    global code_pipeline
    
    try:
        if code_pipeline is None:
            result = plan_pipeline.step(message)
            if result["mode"] == 0:
                emit('bot_response', {'type': 'plan', 'content': str(result["plan"]["游戏策划"]["游戏玩法"])})
                code_pipeline = CodePipeline(result["plan"])
                code_result = code_pipeline.init_step()
                save_code_files(code_result["code"])
                emit('bot_response', {'type': 'code', 'content': "代码已生成，请查看游戏效果"})
            else:
                emit('bot_response', {'type': 'text', 'content': result["response"]})
        
        else:
            result = code_pipeline.step(message)
            if result["mode"] == 0:
                save_code_files(result["code"])
                emit('bot_response', {'type': 'code', 'content': "代码已更新，请查看最新游戏效果"})
            else:
                emit('bot_response', {'type': 'text', 'content': result["response"]})
                
    except Exception as e:
        emit('bot_response', {'type': 'error', 'content': str(e)})

@socketio.on('restart_pipeline')
def restart_pipeline():
    global plan_pipeline, code_pipeline
    plan_pipeline = PlanPipeline()
    code_pipeline = None
    if os.path.exists(OUTPUT_DIR):
        for filename in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    create_output_dir()
    emit('bot_response', {'type': 'info', 'content': "Retainer 已重启"})

def save_code_files(code_dict):
    for filename, content in code_dict.items():
        with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    socketio.run(app, debug=True)
