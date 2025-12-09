#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

root = Path('.')
files = sorted([p for p in root.glob('*.md') if p.name[0].isdigit()])

duplicates = []
for p in files:
    num = int(p.name.split()[0])
    if num >= 9:
        text = p.read_text(encoding='utf-8')
        count = text.count('## Дополнительная информация')
        if count > 1:
            duplicates.append((num, p.name, count))

if duplicates:
    print('Files with duplicates:')
    for num, name, count in duplicates:
        print(f'{num}: {name} - {count} times')
else:
    print('No duplicates found')
