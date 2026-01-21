
import argparse
import shutil
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(description="Initialize AGENTS.md from template")
    parser.add_argument("--template", choices=['base', 'strict', 'flexible'], default='base', help="Template type")
    parser.add_argument("--output", required=True, help="Output path for AGENTS.md")
    
    args = parser.parse_args()
    
    # Locate templates relative to this script
    script_dir = Path(__file__).parent
    template_dir = script_dir.parent / 'assets' / 'templates'
    
    template_map = {
        'base': 'base_agents_md.md',
        'strict': 'strict_agents_md.md',
        'flexible': 'flexible_agents_md.md'
    }
    
    source_file = template_dir / template_map[args.template]
    
    if not source_file.exists():
        print(f"❌ Error: Template file not found at {source_file}")
        sys.exit(1)
        
    try:
        shutil.copy(source_file, args.output)
        print(f"✅ Created AGENTS.md at {args.output} using '{args.template}' template.")
        print("👉 Next step: Open the file and fill in the [TODO] context placeholders.")
    except Exception as e:
        print(f"❌ Error creating file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
