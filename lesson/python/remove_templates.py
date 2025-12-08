"""
Скрипт для удаления шаблонов-заглушек из блока "Дополнительная информация"
"""

import os
import re
from pathlib import Path

def has_template(content):
    """Проверяет, есть ли шаблон-заглушка"""
    template_markers = [
        '# Пример кода, демонстрирующий основные концепции',
        '# из этого урока',
        '# Более сложный пример с комбинированием'
    ]
    return all(marker in content for marker in template_markers)

def remove_template_section(content):
    """Удаляет блок с шаблоном-заглушкой"""
    # Найти начало блока "Дополнительная информация"
    pattern = r'## 📚 Дополнительная информация\n\n.*?(?=\n\n\n|$)'
    
    # Заменяем шаблон на пустую заглушку без содержимого
    replacement = '''## 📚 Дополнительная информация

_Этот раздел будет дополнен практическими примерами и дополнительной информацией._'''
    
    # Используем более точный паттерн для поиска всего блока
    match = re.search(r'## 📚 Дополнительная информация\n\n.+', content, re.DOTALL)
    
    if match:
        # Удаляем весь блок от "Дополнительная информация" до конца
        before_section = content[:match.start()]
        # Добавляем новую короткую заглушку
        new_content = before_section.rstrip() + '\n\n' + replacement + '\n'
        return new_content
    
    return content

def process_file(filepath):
    """Обрабатывает один файл"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if has_template(content):
        new_content = remove_template_section(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    
    return False

def main():
    """Главная функция"""
    lesson_dir = Path(__file__).parent
    
    # Находим все файлы уроков (начинаются с цифры)
    lesson_files = sorted([
        f for f in lesson_dir.glob('*.md')
        if f.name[0].isdigit()
    ], key=lambda x: int(re.match(r'(\d+)', x.name).group(1)))
    
    print(f"Найдено файлов уроков: {len(lesson_files)}\n")
    
    processed_count = 0
    
    for lesson_file in lesson_files:
        if process_file(lesson_file):
            processed_count += 1
            print(f"✓ Обработан: {lesson_file.name}")
    
    print(f"\n{'='*80}")
    print(f"\nИтого обработано файлов: {processed_count}")
    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()
