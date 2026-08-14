import re

def update_tsv_order():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the line starting with const tsv = 
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'const tsv =' in line and '${title}' in line:
            lines[i] = '            const tsv = `${process}\\t\\t\\t\\tIn Progress\\t工程タスク\\t${title}\\t${dateRange}\\t${worker}`;'
            break
            
    with open(path, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))
    print("Updated TSV order.")

if __name__ == "__main__":
    update_tsv_order()
