#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path('.')
files = sorted([p for p in root.glob('*.md') if p.name[0].isdigit()])

fixed = []
for p in files:
    num = int(p.name.split()[0])
    if num >= 9:
        text = p.read_text(encoding='utf-8')
        original = text
        
        # Удаляем жирную ссылку на дополнительную информацию
        # Ищем паттерн: **[Дополнительная информация](#дополнительная-информация)**
        # или **[[#Дополнительная информация]](#дополнительная-информация)**
        pattern1 = r'\*\*\[Дополнительная информация\]\(#дополнительная-информация\)\*\*\n?'
        pattern2 = r'\*\*\[\[#Дополнительная информация\]\]\(#дополнительная-информация\)\*\*\n?'
        
        text = re.sub(pattern1, '', text)
        text = re.sub(pattern2, '', text)
        
        if text != original:
            p.write_text(text, encoding='utf-8')
            fixed.append((num, p.name))

if fixed:
    print(f'Fixed {len(fixed)} files:')
    for num, name in fixed:
        print(f'  {num}: {name}')
else:
    print('No files needed fixing')
