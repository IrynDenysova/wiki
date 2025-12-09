#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

root = Path('.')
files = sorted([p for p in root.glob('*.md') if p.name[0].isdigit()])

stub_files = []
for p in files:
    num = int(p.name.split()[0])
    if num >= 12:
        text = p.read_text(encoding='utf-8')
        if '## Дополнительная информация' in text:
            # Проверяем, есть ли заглушка
            if 'будет дополнен' in text or 'Этот раздел будет' in text:
                stub_files.append((num, p.name))

print(f'Файлы с заглушкой ({len(stub_files)}):')
for num, name in stub_files:
    print(f'  {num}: {name}')
