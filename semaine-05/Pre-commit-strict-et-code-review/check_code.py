import re
import sys

p_print = re.compile(r"\bprint\s*\(")
p_todo = re.compile(r"#\s*TODO(?!\(\w+\):)")
failed = False

for path in sys.argv[1:]:
    if path.endswith("check_code.py"):
        continue

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if p_print.search(line):
                sys.stdout.write(
                    f"[REJETÉ] {path}:{i} - print() interdit. Utilisez logging.\n"
                )
                failed = True
            if p_todo.search(line):
                sys.stdout.write(
                    f"[REJETÉ] {path}:{i} - TODO non attribué. Format requis: # TODO(nom): description\n"
                )
                failed = True

if failed:
    sys.exit(1)
