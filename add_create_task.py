import re

def add_create_task():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Wrap tab-bar
    target_tabbar = """<div class="tab-bar">
            <button class="tab-btn" data-tab="truoc" onclick="switchTab('truoc')">{{ t.tab0 }}</button>
            <button class="tab-btn active" data-tab="nay" onclick="switchTab('nay')">{{ t.tab1 }}</button>
            <button class="tab-btn" data-tab="sau" onclick="switchTab('sau')">{{ t.tab2 }}</button>
        </div>"""
    
    new_tabbar = """<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-md);">
            <div class="tab-bar" style="margin-bottom: 0;">
                <button class="tab-btn" data-tab="truoc" onclick="switchTab('truoc')">{{ t.tab0 }}</button>
                <button class="tab-btn active" data-tab="nay" onclick="switchTab('nay')">{{ t.tab1 }}</button>
                <button class="tab-btn" data-tab="sau" onclick="switchTab('sau')">{{ t.tab2 }}</button>
            </div>
            <button class="btn-primary" onclick="openCreateTaskModal()" style="padding: 8px 16px; border-radius: var(--radius-md); font-weight: 600; display: flex; align-items: center; gap: 6px;">
                <i class="fas fa-plus"></i> {{ 'Tạo Task' if lang == 'vi' else 'タスク作成' }}
            </button>
        </div>"""
    
    if target_tabbar in content:
        content = content.replace(target_tabbar, new_tabbar)
    else:
        print("Could not find tab-bar")
        
    # 2. Add Modal HTML at the very end of body before </body>
    modal_html = """
    <!-- Modal Tạo Task -->
    <div class="drawer-overlay" id="create-task-modal-overlay" onclick="closeCreateTaskModal()" style="z-index: 1050;"></div>
    <div class="modal" id="create-task-modal" style="z-index: 1051;">
        <div class="modal-header">
            <h3>{{ 'Tạo Task mới' if lang == 'vi' else '新規タスク作成' }}</h3>
            <button class="btn-close" onclick="closeCreateTaskModal()">&times;</button>
        </div>
        <div class="modal-body" style="padding: 20px;">
            <div style="margin-bottom: 15px;">
                <label style="display: block; font-weight: bold; margin-bottom: 5px; color: var(--text);">{{ 'Tên tác phẩm' if lang == 'vi' else '作品名' }}</label>
                <input type="text" id="ct-title" class="filter-input" placeholder="Ví dụ: 4巻_スローループ" style="width: 100%; border: 1px solid var(--border); border-radius: 4px; padding: 8px; background: var(--bg-card); color: var(--text);">
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display: block; font-weight: bold; margin-bottom: 5px; color: var(--text);">{{ 'Người thực hiện' if lang == 'vi' else '作業者' }}</label>
                <select id="ct-worker" class="filter-input" style="width: 100%; border: 1px solid var(--border); border-radius: 4px; padding: 8px; background: var(--bg-card); color: var(--text);">
                    <option value="">-- {{ 'Chọn người thực hiện' if lang == 'vi' else '作業者を選択' }} --</option>
                    {% for k, v in user_profiles.items() %}
                        <option value="{{ v.fullname if v.fullname else k }}">{{ v.fullname if v.fullname else k }}</option>
                    {% endfor %}
                </select>
                <small style="color: var(--text-muted); font-size: 12px; margin-top: 4px; display: block;">* Tên này sẽ được copy y hệt để dán vào Notion. (Ví dụ: Phan Duy Tan (タン - Retouch))</small>
            </div>
            <div style="margin-bottom: 15px; display: flex; gap: 15px;">
                <div style="flex: 1;">
                    <label style="display: block; font-weight: bold; margin-bottom: 5px; color: var(--text);">{{ 'Ngày bắt đầu' if lang == 'vi' else '開始日' }}</label>
                    <input type="date" id="ct-start" class="filter-input" style="width: 100%; border: 1px solid var(--border); border-radius: 4px; padding: 8px; background: var(--bg-card); color: var(--text);">
                </div>
                <div style="flex: 1;">
                    <label style="display: block; font-weight: bold; margin-bottom: 5px; color: var(--text);">{{ 'Ngày kết thúc' if lang == 'vi' else '終了日' }}</label>
                    <input type="date" id="ct-end" class="filter-input" style="width: 100%; border: 1px solid var(--border); border-radius: 4px; padding: 8px; background: var(--bg-card); color: var(--text);">
                </div>
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display: block; font-weight: bold; margin-bottom: 5px; color: var(--text);">{{ 'Ngày giao' if lang == 'vi' else '納品日' }}</label>
                <input type="date" id="ct-deadline" class="filter-input" style="width: 100%; border: 1px solid var(--border); border-radius: 4px; padding: 8px; background: var(--bg-card); color: var(--text);">
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display: block; font-weight: bold; margin-bottom: 5px; color: var(--text);">{{ 'Công đoạn' if lang == 'vi' else '関連工程' }}</label>
                <select id="ct-process" class="filter-input" style="width: 100%; border: 1px solid var(--border); border-radius: 4px; padding: 8px; background: var(--bg-card); color: var(--text);">
                    <option value="Prep">Prep</option>
                    <option value="Retouch">Retouch</option>
                    <option value="写植">写植 (Lettering)</option>
                    <option value="Prep, Retouch">Prep, Retouch</option>
                </select>
            </div>
            <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 25px;">
                <button class="btn-outline" onclick="closeCreateTaskModal()" style="padding: 8px 16px;">{{ 'Hủy' if lang == 'vi' else 'キャンセル' }}</button>
                <button class="btn-primary" onclick="copyTaskToNotion()" style="padding: 8px 16px; border-radius: var(--radius-md);">
                    <i class="fas fa-copy"></i> {{ 'Copy dữ liệu cho Notion' if lang == 'vi' else 'Notionにコピー' }}
                </button>
            </div>
        </div>
    </div>
    <script>
        function openCreateTaskModal() {
            document.getElementById('create-task-modal-overlay').classList.add('open');
            document.getElementById('create-task-modal').classList.add('open');
        }
        function closeCreateTaskModal() {
            document.getElementById('create-task-modal-overlay').classList.remove('open');
            document.getElementById('create-task-modal').classList.remove('open');
        }
        function copyTaskToNotion() {
            const title = document.getElementById('ct-title').value;
            const worker = document.getElementById('ct-worker').value;
            
            // Format dates from YYYY-MM-DD to YYYY/MM/DD
            let start = document.getElementById('ct-start').value;
            let end = document.getElementById('ct-end').value;
            if(start) start = start.replace(/-/g, '/');
            if(end) end = end.replace(/-/g, '/');
            
            let dateRange = "";
            if(start && end) {
                dateRange = start + " → " + end;
            } else if (start) {
                dateRange = start;
            }
            
            let deadline = document.getElementById('ct-deadline').value;
            if(deadline) deadline = deadline.replace(/-/g, '/');
            
            const process = document.getElementById('ct-process').value;
            
            // Notion Order: Title, Status, Worker, DateRange, Deadline, Process, QC, Completion
            const status = "In Progress";
            const qc = "";
            const completion = "";
            
            const tsv = `${title}\\t${status}\\t${worker}\\t${dateRange}\\t${deadline}\\t${process}\\t${qc}\\t${completion}`;
            
            navigator.clipboard.writeText(tsv).then(() => {
                showToast(CURRENT_LANG === 'vi' ? 'Đã copy thành công! Hãy dán (Ctrl+V) vào dòng mới trên Notion.' : 'コピーしました！Notionに貼り付けてください。', 'success');
                closeCreateTaskModal();
            }).catch(err => {
                console.error('Copy failed', err);
                showToast(CURRENT_LANG === 'vi' ? 'Lỗi khi copy!' : 'コピー失敗！', 'error');
            });
        }
    </script>
    """
    
    if "create-task-modal" not in content:
        content = content.replace("</body>", modal_html + "\n</body>")
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
if __name__ == "__main__":
    add_create_task()
