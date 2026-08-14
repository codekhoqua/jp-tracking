import re

def fix_copy_bug():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update the button to use data- attributes instead of JSON payload
    old_btn_pattern = re.compile(r'<button class="btn-primary" onclick="copyNotionTask\(this\)" data-row=".*?">.*?</button>', re.DOTALL)
    
    new_btn = """<button class="btn-primary" 
                data-process="{{ row.get('Công đoạn', row.get('Job', ''))|e }}"
                data-title="{{ tp_name_display|e }}"
                data-start="{{ row.get('Ngày bắt đầu (Dự kiến)', '')|e }}"
                data-end="{{ row.get('Ngày kết thúc (Dự kiến)', '')|e }}"
                data-deadline="{{ row.get('Deadline', row.get('Ngày giao', ''))|e }}"
                data-worker="{{ worker|e }}"
                onclick="copyNotionTask(this)" 
                style="font-size: 12px; padding: 4px 10px; border-radius: 4px; display: flex; align-items: center; gap: 6px; margin-right: 15px; border: none; cursor: pointer; transition: all 0.2s; background: rgba(16, 185, 129, 0.15); color: #10b981;">
                <i class="fas fa-copy"></i> {{ 'Copy Notion' if lang == 'vi' else 'Notionコピー' }}
            </button>"""
            
    if old_btn_pattern.search(content):
        content = old_btn_pattern.sub(new_btn, content)
        
    # 2. Update the JS function
    old_js_pattern = re.compile(r'function copyNotionTask\(btn\) \{.*?\n    \}', re.DOTALL)
    
    new_js = """function copyNotionTask(btn) {
        try {
            const process = btn.dataset.process || '';
            const title = btn.dataset.title || '';
            const worker = btn.dataset.worker || '';
            let start = btn.dataset.start || '';
            let end = btn.dataset.end || '';
            let deadline = btn.dataset.deadline || '';
            
            // Clean up NaN strings from Pandas
            if(start.toLowerCase() === 'nan') start = '';
            if(end.toLowerCase() === 'nan') end = '';
            if(deadline.toLowerCase() === 'nan') deadline = '';
            if(worker.toLowerCase() === 'nan') worker = '';
            
            let dateRange = "";
            let startFmt = start.replace(/-/g, '/');
            let endFmt = end.replace(/-/g, '/');
            
            if(startFmt && endFmt) {
                dateRange = startFmt + " → " + endFmt;
            } else if (startFmt) {
                dateRange = startFmt;
            }
            
            // Format TSV to match Notion Table View exactly
            const tsv = `${process}\\t\\t\\t\\tIn Progress\\t工程タスク\\t${title}\\t${dateRange}\\t${worker}`;
            
            navigator.clipboard.writeText(tsv).then(() => {
                showToast(CURRENT_LANG === 'vi' ? 'Đã copy thành công! Hãy sang Notion dán (Ctrl+V).' : 'コピーしました！Notionに貼り付けてください。', 'success');
            }).catch(err => {
                console.error('Copy failed', err);
                showToast(CURRENT_LANG === 'vi' ? 'Lỗi khi copy!' : 'コピー失敗！', 'error');
            });
        } catch (e) {
            console.error("Error formatting TSV:", e);
            showToast('Lỗi JS!', 'error');
        }
    }"""
    
    if old_js_pattern.search(content):
        content = old_js_pattern.sub(new_js, content)
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed copy bug.")

if __name__ == "__main__":
    fix_copy_bug()
