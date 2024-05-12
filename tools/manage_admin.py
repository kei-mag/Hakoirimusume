import sys
from pathlib import Path

script_name = Path(__file__).name
help_text = f"""Manage admin users of Hakoirimusume

Usage: 
Add admin user(s):
    python {script_name} add <userid> ...

Remove admin user(s):
    python {script_name} remove <userid>...
"""

if __name__ == "__main__":
    if len(sys.argv) < 2 or "--help" in sys.argv or "-h" in sys.argv:
        print(help_text)
        sys.exit(0)
