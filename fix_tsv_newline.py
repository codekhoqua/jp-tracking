import re

def fix_tsv_newline():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the TSV generation and add \n at the end
    old_js_pattern = re.compile(r'const tsv = `\$\{process\}\\t\$\{empty\}.*?\$\{worker\}`;', re.DOTALL)
    
    # We add \n at the end to force Notion to recognize it as a spreadsheet row
    new_js = """const tsv = `${process}\\t${empty}\\t${empty}\\t${empty}\\tIn Progress\\t工程タスク\\t${title}\\t${dateRange}\\t${worker}\\n`;"""
    
    if old_js_pattern.search(content):
        content = old_js_pattern.sub(new_js, content)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed TSV newline.")
    else:
        print("Could not find pattern.")

if __name__ == "__main__":
    fix_tsv_newline()
