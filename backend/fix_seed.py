with open("seed.py", "r", encoding="utf-8") as f:
    content = f.read()
fixed = 0
for price in [
    "27.00",
    "29.00",
    "17.00",
    "24.99",
    "8.00",
    "12.99",
    "30.00",
    "15.00",
    "35.00",
    "24.99",
    "32.00",
    "29.99",
    "32.00",
    "18.00",
    "22.00",
    "29.99",
    "19.99",
    "26.00",
    "20.00",
    "13.00",
    "34.00",
    "25.00",
    "30.00",
    "28.00",
    "24.00",
]:
    old = f'Decimal("{price}",'
    new = f'Decimal("{price}"),'
    if old in content:
        content = content.replace(old, new)
        fixed += 1
with open("seed.py", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Fixed {fixed} occurrences")
