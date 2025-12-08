"""
Скрипт для проверки уроков Python:
1. Проверка навигационных ссылок
2. Проверка наличия блока "Дополнительная информация"
"""

import os
import re
from pathlib import Path

def extract_anchor_from_link(link):
    """Извлекает якорь из ссылки markdown"""
    match = re.search(r'\(#([^)]+)\)', link)
    return match.group(1) if match else None

def find_headers_in_file(content):
    """Находит все заголовки в файле и их якоря"""
    headers = {}
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Ищем заголовки ## или ###
        if line.strip().startswith('#'):
            # Удаляем # и получаем текст заголовка
            header_text = line.strip().lstrip('#').strip()
            # Генерируем якорь так, как это делает markdown
            anchor = generate_anchor(header_text)
            headers[anchor] = {
                'line': i,
                'text': header_text,
                'level': len(line) - len(line.lstrip('#'))
            }
    return headers

def generate_anchor(text):
    """Генерирует якорь из текста заголовка по правилам markdown"""
    # Убираем markdown форматирование
    text = re.sub(r'[`*_]', '', text)
    # Приводим к нижнему регистру
    text = text.lower()
    # Заменяем пробелы и специальные символы на дефисы
    text = re.sub(r'[^\w\u0400-\u04FF\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = text.strip('-')
    return text

def find_navigation_links(content):
    """Находит все навигационные ссылки в начале файла"""
    links = []
    lines = content.split('\n')
    in_navigation = False
    
    for i, line in enumerate(lines, 1):
        # Начало навигации
        if '📖 Быстрая навигация' in line:
            in_navigation = True
            continue
        
        # Конец навигации
        if in_navigation and line.strip().startswith('**[📚'):
            break
        
        # Извлекаем ссылки из навигации
        if in_navigation and '](' in line:
            anchor = extract_anchor_from_link(line)
            if anchor:
                links.append({
                    'line': i,
                    'anchor': anchor,
                    'text': line.strip()
                })
    
    return links

def check_additional_info_section(content):
    """Проверяет, есть ли полноценный блок 'Дополнительная информация'"""
    # Ищем заголовок блока
    if '## 📚 Дополнительная информация' not in content:
        return {
            'exists': False,
            'is_template': False,
            'message': 'Блок "Дополнительная информация" отсутствует'
        }
    
    # Проверяем, является ли это заглушкой
    template_markers = [
        '# Пример кода, демонстрирующий основные концепции',
        '# из этого урока',
        '# Более сложный пример с комбинированием'
    ]
    
    is_template = all(marker in content for marker in template_markers)
    
    return {
        'exists': True,
        'is_template': is_template,
        'message': 'Используется шаблон-заглушка' if is_template else 'Блок заполнен'
    }

def check_lesson_file(filepath):
    """Проверяет один файл урока"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    issues = []
    
    # 1. Проверяем навигационные ссылки
    nav_links = find_navigation_links(content)
    headers = find_headers_in_file(content)
    
    broken_links = []
    for link in nav_links:
        if link['anchor'] not in headers:
            broken_links.append(f"  ❌ Строка {link['line']}: #{link['anchor']} -> заголовок не найден")
    
    if broken_links:
        issues.append("\n🔗 Проблемы с навигацией:")
        issues.extend(broken_links)
    
    # 2. Проверяем блок "Дополнительная информация"
    additional_info = check_additional_info_section(content)
    if not additional_info['exists']:
        issues.append(f"\n📚 {additional_info['message']}")
    elif additional_info['is_template']:
        issues.append(f"\n📚 ⚠️  {additional_info['message']}")
    
    return {
        'filename': filename,
        'issues': issues,
        'nav_links_count': len(nav_links),
        'headers_count': len(headers),
        'has_issues': len(issues) > 0,
        'additional_info': additional_info
    }

def main():
    """Главная функция"""
    lesson_dir = Path(__file__).parent
    
    # Находим все файлы уроков (начинаются с цифры)
    lesson_files = sorted([
        f for f in lesson_dir.glob('*.md')
        if f.name[0].isdigit()
    ], key=lambda x: int(re.match(r'(\d+)', x.name).group(1)))
    
    print(f"Найдено файлов уроков: {len(lesson_files)}\n")
    print("=" * 80)
    
    all_results = []
    files_with_issues = []
    files_with_templates = []
    
    for lesson_file in lesson_files:
        result = check_lesson_file(lesson_file)
        all_results.append(result)
        
        if result['has_issues']:
            files_with_issues.append(result['filename'])
            print(f"\n📄 {result['filename']}")
            for issue in result['issues']:
                print(issue)
            print("-" * 80)
        
        if result['additional_info']['is_template']:
            files_with_templates.append(result['filename'])
    
    # Итоговая статистика
    print("\n" + "=" * 80)
    print("\n📊 ИТОГОВАЯ СТАТИСТИКА:\n")
    print(f"Всего файлов проверено: {len(all_results)}")
    print(f"Файлов без проблем: {len(all_results) - len(files_with_issues)}")
    print(f"Файлов с проблемами: {len(files_with_issues)}")
    print(f"Файлов с шаблоном-заглушкой: {len(files_with_templates)}")
    
    if files_with_templates:
        print(f"\n⚠️  Файлы с шаблоном-заглушкой:")
        for filename in files_with_templates:
            print(f"  - {filename}")
    
    if not files_with_issues:
        print("\n✅ Все файлы в порядке!")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
