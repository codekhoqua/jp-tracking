import re

def fix_task_button():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Revert the tab-bar
    bad_tabbar = """<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-md);">
            <div class="tab-bar" style="margin-bottom: 0;">
                <button class="tab-btn" data-tab="truoc" onclick="switchTab('truoc')">{{ t.tab0 }}</button>
                <button class="tab-btn active" data-tab="nay" onclick="switchTab('nay')">{{ t.tab1 }}</button>
                <button class="tab-btn" data-tab="sau" onclick="switchTab('sau')">{{ t.tab2 }}</button>
            </div>
            <button class="btn-primary" onclick="openCreateTaskModal()" style="padding: 8px 16px; border-radius: var(--radius-md); font-weight: 600; display: flex; align-items: center; gap: 6px;">
                <i class="fas fa-plus"></i> {{ 'Tạo Task' if lang == 'vi' else 'タスク作成' }}
            </button>
        </div>"""
        
    good_tabbar = """<div class="tab-bar">
            <button class="tab-btn" data-tab="truoc" onclick="switchTab('truoc')">{{ t.tab0 }}</button>
            <button class="tab-btn active" data-tab="nay" onclick="switchTab('nay')">{{ t.tab1 }}</button>
            <button class="tab-btn" data-tab="sau" onclick="switchTab('sau')">{{ t.tab2 }}</button>
        </div>"""
        
    if bad_tabbar in content:
        content = content.replace(bad_tabbar, good_tabbar)
        
    # 2. Remove the modal
    modal_start = "<!-- Modal Tạo Task -->"
    modal_end = "function copyTaskToNotion() {"
    if modal_start in content:
        content = re.sub(r'<!-- Modal Tạo Task -->.*?</script>', '', content, flags=re.DOTALL)
        
    # 3. Add button to task modal header
    target_close = """            <button class="close-btn" onclick="closeModal('{{ tab_key }}-{{ loop.index0 }}', '{{ tp_key }}')">"""
    new_close = """            <button class="btn-primary" onclick="copyNotionTask('{{ row|tojson|forceescape }}')" style="font-size: 12px; padding: 4px 10px; border-radius: 4px; display: flex; align-items: center; gap: 6px; margin-right: 15px; border: none; cursor: pointer; transition: all 0.2s; background: rgba(16, 185, 129, 0.15); color: #10b981;">
                <i class="fas fa-copy"></i> {{ 'Copy Notion' if lang == 'vi' else 'Notionコピー' }}
            </button>
            <button class="close-btn" onclick="closeModal('{{ tab_key }}-{{ loop.index0 }}', '{{ tp_key }}')">"""
    
    if "copyNotionTask(" not in content:
        content = content.replace(target_close, new_close)
        
    # 4. Add the copyNotionTask JS function
    js_func = """
    <script>
    function copyNotionTask(rowJson) {
        try {
            const row = JSON.parse(rowJson);
            const title = row['Tên tác phẩm'] || row['Task Name'] || row['name'] || row['tp_name'] || '';
            const worker = row['Người thực hiện'] || row['Worker'] || '';
            
            const start = row['Ngày bắt đầu (Dự kiến)'] || row['Ngày bắt đầu'] || '';
            const end = row['Ngày kết thúc (Dự kiến)'] || row['Ngày kết thúc'] || '';
            const deadline = row['Deadline'] || row['Ngày giao (Dự kiến)'] || row['Ngày giao'] || '';
            const process = row['Công đoạn'] || row['Job'] || row['JobType'] || '';
            
            let dateRange = "";
            let startFmt = start.replace(/-/g, '/');
            let endFmt = end.replace(/-/g, '/');
            
            if(startFmt && endFmt) {
                dateRange = startFmt + " → " + endFmt;
            } else if (startFmt) {
                dateRange = startFmt;
            }
            
            const status = "In Progress";
            const qc = "";
            const completion = "";
            
            // Format TSV
            const tsv = `${title}\\t${status}\\t${worker}\\t${dateRange}\\t${deadline.replace(/-/g, '/')}\\t${process}\\t${qc}\\t${completion}`;
            
            navigator.clipboard.writeText(tsv).then(() => {
                showToast(CURRENT_LANG === 'vi' ? 'Đã copy thành công! Hãy sang Notion dán (Ctrl+V).' : 'コピーしました！Notionに貼り付けてください。', 'success');
            }).catch(err => {
                console.error('Copy failed', err);
                showToast(CURRENT_LANG === 'vi' ? 'Lỗi khi copy!' : 'コピー失敗！', 'error');
            });
        } catch (e) {
            console.error("Error parsing row data:", e);
            showToast('Error', 'error');
        }
    }
    </script>
    """
    
    if "function copyNotionTask(" not in content:
        content = content.replace("</body>", js_func + "\n</body>")
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed task button placement.")

if __name__ == "__main__":
    fix_task_button()
