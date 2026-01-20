import os
import sys
from datetime import datetime

def init_notebook(session_name, base_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"research_{session_name}_{timestamp}"
    folder_path = os.path.join(base_path, folder_name)
    
    os.makedirs(folder_path, exist_ok=True)
    
    notebook_content = f"""# Research Notebook: {session_name}
Date: {datetime.now().strftime("%Y-%m-%d")}

## Objective
[Insert Research Goal]

## Layers & Iterations
### Layer 1
**Questions:**
- 
**Findings:**
- 

## Conflicting Data & Gaps
- 

## Sources
- 
"""
    
    notebook_path = os.path.join(folder_path, "notebook.md")
    with open(notebook_path, "w", encoding="utf-8") as f:
        f.write(notebook_content)
    
    print(f"Initialized research session at: {folder_path}")
    return folder_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python init_notebook.py <session_name> <base_path>")
    else:
        init_notebook(sys.argv[1], sys.argv[2])
