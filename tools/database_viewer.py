import sys
from pathlib import Path

script_name = Path(__file__).name

help_text = f"""Show database contents of Hakoirimusume
[!WARNING!] This script is for debugging purposes only. Understand the security risks before using it.

Usage: python {script_name} <database-file-path> [options]

Arguments:
    database-file-path                      Path to the database file
    
Options:
    -t, --table <table-name>                Name of the table to show
    -c, --columns <column1> <column2> ...   Names of the columns to show
    -h, --help                              Show this help message and exit
"""

if __name__ == "__main__":
    if len(sys.argv) < 2 or "--help" in sys.argv or "-h" in sys.argv:
        print(help_text)
        sys.exit(0)
