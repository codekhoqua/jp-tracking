import re

def fix_copy_fallback():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update the JS function
    old_js_pattern = re.compile(r'function copyNotionTask\(btn\) \{.*?\n    \}', re.DOTALL)
    
    new_js = """function copyNotionTask(btn) {
        try {
            const process = btn.dataset.process || '';
            const title = btn.dataset.title || '';
            const worker = btn.dataset.worker || '';
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
            
            // Format TSV
            const tsv = `${process}\\t\\t\\t\\tIn Progress\\t工程タスク\\t${title}\\t${dateRange}\\t${worker}`;
            
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
    print("Fixed copy fallback.")

if __name__ == "__main__":
    fix_copy_fallback()
