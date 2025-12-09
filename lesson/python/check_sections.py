#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

root = Path('.')
files = sorted([p for p in root.glob('*.md') if p.name[0].isdigit()])

has_section = []
missing_section = []

for p in files:
    num = int(p.name.split()[0])
    if num >= 9:
        text = p.read_text(encoding='utf-8')
        if '## Дополнительная информация' in text:
            has_section.append((num, p.name))
        else:
            missing_section.append((num, p.name))

print(f"✅ Есть раздел ({len(has_section)}):")
for num, name in has_section:
    print(f"  {num}: {name}")

print(f"\n❌ Нет раздела ({len(missing_section)}):")
for num, name in missing_section:
    print(f"  {num}: {name}")
