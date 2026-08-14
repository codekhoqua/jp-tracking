import re

def fix_tsv_process():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the JS block
    old_js_pattern = re.compile(r'function copyNotionTask\(btn\) \{.*?\n    \}', re.DOTALL)
    
    new_js = """function copyNotionTask(btn) {
        try {
            let title = btn.dataset.title || '';
            let worker = btn.dataset.worker || '';
            let start = btn.dataset.start || '';
            let end = btn.dataset.end || '';
            let deadline = btn.dataset.deadline || '';
            
            // Clean up NaN strings
            if(start.toLowerCase() === 'nan') start = '';
            if(end.toLowerCase() === 'nan') end = '';
            if(deadline.toLowerCase() === 'nan') deadline = '';
            
            let dateRange = "";
            let startFmt = start.replace(/-/g, '/');
            let endFmt = end.replace(/-/g, '/');
            
            if(startFmt && endFmt) {
                dateRange = startFmt + " → " + endFmt;
            } else if (startFmt) {
                dateRange = startFmt;
            }
            
            // Extract process and clean title (e.g. "Prep - 12_MUJIN" -> process="Prep", title="12_MUJIN")
            let process = "Prep";
            if(title.includes(' - ')) {
                process = title.split(' - ')[0].trim();
                title = title.substring(title.indexOf(' - ') + 3).trim();
            }
            
            // Ensure no empty strings cause Notion to strip tabs. We use a space " " instead of ""
            const empty = " ";
            
            // Format TSV to match Notion Table View exactly
            // 1: 工程名 (Process)
            // 2: QC依頼 (Empty)
            // 3: QC者 (Empty)
            // 4: done (Empty checkbox)
            // 5: ステータス (In Progress)
            // 6: タスクの種類 (工程タスク)
            // 7: 作品名 (Title)
            // 8: 作業日程 (DateRange)
            // 9: 作業者 (Worker)
            const tsv = `${process}\\t${empty}\\t${empty}\\t${empty}\\tIn Progress\\t工程タスク\\t${title}\\t${dateRange}\\t${worker}`;
            
            // Fallback copy for HTTP
            const fallbackCopy = (text) => {
                const textArea = document.createElement("textarea");
                textArea.value = text;
                textArea.style.top = "0";
                textArea.style.left = "0";
                textArea.style.position = "fixed";
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                try {
                    const successful = document.execCommand('copy');
                    if(successful) {
                        alert("Đã Copy thành công! Mời bạn sang Notion dán (Ctrl+V)");
                    } else {
                        alert("Không thể Copy! Trình duyệt của bạn chặn tính năng này.");
                    }
                } catch (err) {
                    alert("Lỗi Copy: " + err);
                }
                document.body.removeChild(textArea);
            };
            
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(tsv).then(() => {
                    alert("Đã Copy thành công! Mời bạn sang Notion dán (Ctrl+V)");
                }).catch(err => {
                    fallbackCopy(tsv);
                });
            } else {
                fallbackCopy(tsv);
            }
        } catch (e) {
            console.error("Error formatting TSV:", e);
            alert('Có lỗi xảy ra khi xử lý dữ liệu: ' + e.message);
        }
    }"""
    
    if old_js_pattern.search(content):
        content = old_js_pattern.sub(new_js, content)
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed TSV process logic.")

if __name__ == "__main__":
    fix_tsv_process()
