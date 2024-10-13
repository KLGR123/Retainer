# code running
echo "@RETAINER 游戏开发智能助手 🕹️"
streamlit run app.py plan &
streamlit run app.py code

# used to combine plan and code history json files
plan_history_json='memory/plan_history_cache.json'
code_history_json='memory/code_history_cache.json'

if [[ -f "$plan_history_json" && -f "$code_history_json" ]]; then
    python3 modules/memory/combiner.py
else
    echo "MEMORY: ONE OR BOTH OF THE FILES DO NOT EXIST."
fi