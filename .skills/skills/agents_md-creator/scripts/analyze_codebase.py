
import os
import json
import argparse
from pathlib import Path

def analyze_structure(root_path, max_depth=2):
    structure = []
    root = Path(root_path)
    
    for path in root.rglob('*'):
        if path.is_file():
            rel_path = path.relative_to(root)
            depth = len(rel_path.parts)
            if depth <= max_depth:
                structure.append(str(rel_path))
    return structure

def detect_tech_stack(root_path):
    stack = []
    root = Path(root_path)
    
    if (root / 'package.json').exists():
        stack.append("Node.js")
        try:
            with open(root / 'package.json') as f:
                data = json.load(f)
                deps = data.get('dependencies', {})
                if 'react' in deps: stack.append("React")
                if 'next' in deps: stack.append("Next.js")
                if 'typescript' in deps or (root / 'tsconfig.json').exists(): stack.append("TypeScript")
        except:
            pass

    if (root / 'requirements.txt').exists() or (root / 'pyproject.toml').exists():
        stack.append("Python")
        
    if (root / 'Cargo.toml').exists():
        stack.append("Rust")
        
    if (root / 'go.mod').exists():
        stack.append("Go")

    return stack

def detect_docs(root_path):
    docs = []
    root = Path(root_path)
    possible_docs = ['README.md', 'CONTRIBUTING.md', 'docs/']
    
    for d in possible_docs:
        if (root / d).exists():
            docs.append(str(d))
            
    return docs

def main():
    parser = argparse.ArgumentParser(description="Analyze codebase for AGENTS.md context")
    parser.add_argument("--path", required=True, help="Path to repository root")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    
    args = parser.parse_args()
    
    repo_path = Path(args.path)
    if not repo_path.exists():
        print(f"Error: Path {repo_path} does not exist.")
        return

    context = {
        "structure_preview": analyze_structure(repo_path),
        "tech_stack": detect_tech_stack(repo_path),
        "existing_docs": detect_docs(repo_path),
        "repo_name": repo_path.name
    }
    
    with open(args.output, 'w') as f:
        json.dump(context, f, indent=2)
        
    print(f"✅ Analysis complete. Context saved to {args.output}")

if __name__ == "__main__":
    main()
