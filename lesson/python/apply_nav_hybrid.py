import re
from pathlib import Path


def slug(title: str) -> str:
    t = title.strip().lower()
    t = re.sub(r'[`*_~]', '', t)
    t = re.sub(r"[~`!@#$%^&*()\[\]{}|;:'\",.<>?/+=]", '', t)
    t = re.sub(r'\s+', '-', t)
    t = re.sub(r'-+', '-', t).strip('-')
    return t


def build_nav(lines: list[str]) -> tuple[list[str], bool]:
    nav = []
    has_additional = False
    for line in lines:
        if line.startswith('## '):
            title = line.lstrip('#').strip()
            if title.startswith('📖'):
                continue
            if 'дополнительная информация' in title.lower():
                has_additional = True
            nav.append((title, slug(title)))
    nav_lines = [f"- [[#{title}]](#{anchor})" for title, anchor in nav]
    return nav_lines, has_additional


def transform_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()

    nav_lines, has_additional = build_nav(lines)
    if has_additional:
        nav_lines.append("")
        nav_lines.append("**[[#📚 Дополнительная информация]](#дополнительная-информация)**")

    out = []
    i = 0
    changed = False
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('## 📖 Быстрая навигация'):
            # write new nav block
            out.append(line)
            out.append('')
            out.extend(nav_lines)
            out.append('')
            changed = True
            # skip old nav until first '---'
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('---'):
                i += 1
            if i < len(lines):
                out.append(lines[i])  # append the '---'
            i += 1
            continue
        out.append(line)
        i += 1

    if changed:
        path.write_text('\n'.join(out) + ('\n' if text.endswith('\n') else ''), encoding='utf-8')
    return changed


def main():
    root = Path(__file__).parent
    files = sorted([p for p in root.glob('*.md') if p.name[0].isdigit()])
    total = 0
    for p in files:
        if transform_file(p):
            total += 1
            print(f"updated: {p.name}")
    print(f"done. modified {total} files")


if __name__ == '__main__':
    main()
