import re

def fix_html_clipboard():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_js_pattern = re.compile(r'<script>\nfunction copyNotionTask.*?<\/script>', re.DOTALL)
    
    new_js = """<script>
function copyNotionTask(btn) {
    try {
        let title = btn.dataset.title || '';
        let worker = btn.dataset.worker || '';
        let start = btn.dataset.start || '';
        let end = btn.dataset.end || '';
        let deadline = btn.dataset.deadline || '';
        
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
        
        let process = "Prep";
        if(title.includes(' - ')) {
            process = title.split(' - ')[0].trim();
            title = title.substring(title.indexOf(' - ') + 3).trim();
        }
        
        // Build the HTML table string for Notion
        // Notion REQUIRES an HTML table structure in the clipboard to paste into multiple columns
        const html = `<table>
            <tr>
                <td>${process}</td>
                <td></td>
                <td></td>
                <td></td>
                <td>In Progress</td>
                <td>工程タスク</td>
                <td>${title}</td>
                <td>${dateRange}</td>
                <td>${worker}</td>
            </tr>
        </table>`;
        
        const tsv = `${process}\\t\\t\\t\\tIn Progress\\t工程タスク\\t${title}\\t${dateRange}\\t${worker}\\n`;
        
        const fallbackCopyHtml = (htmlStr, textStr) => {
            const div = document.createElement("div");
            div.innerHTML = htmlStr;
            div.style.position = "fixed";
            div.style.top = "0";
            div.style.left = "-9999px";
            document.body.appendChild(div);
            
            const selection = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(div);
            selection.removeAllRanges();
            selection.addRange(range);
            
            try {
                const successful = document.execCommand('copy');
                if(successful) {
                    alert("Đã Copy thành công! Mời bạn sang Notion (Tab VN), CHỈ BẤM 1 LẦN VÀO Ô TRỐNG rồi dán (Ctrl+V)");
                } else {
                    alert("Không thể Copy! Trình duyệt chặn tính năng này.");
                }
            } catch (err) {
                alert("Lỗi Copy: " + err);
            }
            selection.removeAllRanges();
            document.body.removeChild(div);
        };
        
        if (navigator.clipboard && window.ClipboardItem && window.isSecureContext) {
            const blobHtml = new Blob([html], { type: "text/html" });
            const blobText = new Blob([tsv], { type: "text/plain" });
            const data = [new ClipboardItem({ "text/html": blobHtml, "text/plain": blobText })];
            
            navigator.clipboard.write(data).then(() => {
                alert("Đã Copy thành công! Mời bạn sang Notion (Tab VN), CHỈ BẤM 1 LẦN VÀO Ô TRỐNG rồi dán (Ctrl+V)");
            }).catch(err => {
                fallbackCopyHtml(html, tsv);
            });
        } else {
            fallbackCopyHtml(html, tsv);
        }
    } catch (e) {
        console.error("Error formatting TSV:", e);
        alert('Có lỗi xảy ra khi xử lý dữ liệu: ' + e.message);
    }
}
</script>"""
    
    if old_js_pattern.search(content):
        content = old_js_pattern.sub(new_js, content)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed HTML clipboard logic.")
    else:
        print("Pattern not found!")

if __name__ == "__main__":
    fix_html_clipboard()
