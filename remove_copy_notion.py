import re

def remove_copy_notion():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove the button
    button_pattern = re.compile(r'<button class="btn-primary"\s+data-process=".*?onclick="copyNotionTask\(this\)".*?<\/button>', re.DOTALL)
    content = button_pattern.sub('', content)

    # 2. Remove the JS script block
    script_pattern = re.compile(r'<script>\nfunction copyNotionTask.*?<\/script>', re.DOTALL)
    content = script_pattern.sub('', content)
    
    # 3. Bump version
    content = re.sub(r'v1\.1\.86', 'v1.1.87', content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Removed Copy Notion feature and bumped to v1.1.87.")

if __name__ == "__main__":
    remove_copy_notion()
