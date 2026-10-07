with open("seed.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'Decimal("' in line and line.count("(") != line.count(")"):
        print(f"{i}: {line.rstrip()}")
