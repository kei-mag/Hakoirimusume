import re
import sqlite3
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


def view(database_file_path: str, table: str):
    conn = sqlite3.connect(database_file_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    columuns = cur.description
    # Print column names
    name_row = "| " + (" " * 32 + " | ").join([col[0] for col in columuns]) + (" " * 32 + " |")
    print(name_row)
    print("-" * len(name_row))
    # Print rows
    rows = cur.fetchall()
    if not rows:
        print(f"----- Table '{table}' is empty. -----")
    else:
        for row in rows:
            print("| ", end="")
            for col in row:
                print(col, end=" " * (33 - len(str(col))) + " | ")
            print("")


if __name__ == "__main__":
    if len(sys.argv) < 2 or "--help" in sys.argv or "-h" in sys.argv:
        print(help_text)
        sys.exit(0)
    else:
        table_name = re.compile(r"--table|-t (.+)").search(" ".join(sys.argv))
        view(sys.argv[1], table_name.group(1) if table_name else "users")
