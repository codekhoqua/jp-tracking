import re

def fix_json_pass():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix the button
    target_btn = """<button class="btn-primary" onclick="copyNotionTask('{{ row|tojson|forceescape }}')" style="font-size: 12px; padding: 4px 10px; border-radius: 4px; display: flex; align-items: center; gap: 6px; margin-right: 15px; border: none; cursor: pointer; transition: all 0.2s; background: rgba(16, 185, 129, 0.15); color: #10b981;">"""
    
    new_btn = """<button class="btn-primary" onclick="copyNotionTask(this)" data-row="{{ row|tojson|forceescape }}" style="font-size: 12px; padding: 4px 10px; border-radius: 4px; display: flex; align-items: center; gap: 6px; margin-right: 15px; border: none; cursor: pointer; transition: all 0.2s; background: rgba(16, 185, 129, 0.15); color: #10b981;">"""
    
    if target_btn in content:
        content = content.replace(target_btn, new_btn)

    # Fix the JS
    target_js = """function copyNotionTask(rowJson) {
        try {
            const row = JSON.parse(rowJson);"""
            
    new_js = """function copyNotionTask(btn) {
        try {
            const row = JSON.parse(btn.dataset.row);"""
            
    if target_js in content:
        content = content.replace(target_js, new_js)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed JS passing")

if __name__ == "__main__":
    fix_json_pass()
