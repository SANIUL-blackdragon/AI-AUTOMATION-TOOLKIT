
import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "Authority",
    "Operating Mode",
    "Safety",
    "Persona",
    "Tech Stack",
    "Boundaries"
]

def validate(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"❌ File not found: {path}")
        return False
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    missing = []
    for section in REQUIRED_SECTIONS:
        # Simple check for section headers (case insensitive fuzzy match)
        if section.lower() not in content.lower():
            missing.append(section)
            
    if missing:
        print("❌ Validation Failed. Missing required sections:")
        for m in missing:
            print(f"  - {m}")
        return False
        
    print("✅ Validation Passed! Structure looks good.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Validate AGENTS.md structure")
    parser.add_argument("--file", required=True, help="Path to AGENTS.md")
    
    args = parser.parse_args()
    validate(args.file)

if __name__ == "__main__":
    main()
