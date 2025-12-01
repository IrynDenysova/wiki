import os
import re
from pathlib import Path
from typing import List, Tuple

from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parents[1]

OUTPUT_FILENAME = "SUMMARY.md"


def extract_text_from_pdf(pdf_path: Path) -> str:
    try:
        reader = PdfReader(str(pdf_path))
        texts = []
        for page in reader.pages:
            texts.append(page.extract_text() or "")
        return "\n".join(texts)
    except Exception as e:
        return f"ERROR reading {pdf_path.name}: {e}"


def clean_text(text: str) -> str:
    if not text:
        return ""
    # Normalize whitespace
    text = re.sub(r"\r\n|\r|\n", "\n", text)
    text = re.sub(r"\u00A0", " ", text)
    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def summarize_text(text: str, max_chars: int = 2000) -> str:
    """
    Very simple heuristic summary: keep title-like lines, first paragraphs, and key bullets.
    This avoids external API usage and works offline.
    """
    if not text:
        return ""
    lines = text.split("\n")

    # pick candidate title lines (short, capitalized)
    titles: List[str] = []
    bullets: List[str] = []
    body: List[str] = []

    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if re.match(r"^[A-Z][A-Za-z0-9 .:_-]{0,80}$", s):
            titles.append(s)
            continue
        if re.match(r"^[-•◦∗*]", s):
            bullets.append(s)
            continue
        body.append(s)

    # build markdown
    md: List[str] = []
    if titles:
        md.append(f"# {titles[0]}")
        for t in titles[1:3]:
            md.append(f"## {t}")
    else:
        md.append("# Сводка PDF")

    # add brief abstract
    abstract = " ".join(body[:5])
    if abstract:
        md.append("\n**Кратко:** " + abstract[:600] + ("…" if len(abstract) > 600 else ""))

    # add bullets
    if bullets:
        md.append("\n**Основные пункты:**")
        for b in bullets[:12]:
            md.append(f"- {b.lstrip('-•*').strip()}")

    # add a trimmed body section
    joined = "\n\n".join(body)
    if joined:
        md.append("\n**Извлечённый текст (обрезано):**\n")
        md.append(joined[:max_chars] + ("\n…" if len(joined) > max_chars else ""))

    return "\n".join(md).strip() + "\n"


def find_pdf_files(folder: Path) -> List[Path]:
    return sorted(p for p in folder.glob("*.pdf"))


def process_folder(folder: Path) -> Tuple[int, Path]:
    pdfs = find_pdf_files(folder)
    if not pdfs:
        return 0, folder / OUTPUT_FILENAME

    parts: List[str] = []
    parts.append(f"# Конспект для папки `{folder.name}`\n")

    for pdf in pdfs:
        text = clean_text(extract_text_from_pdf(pdf))
        summary = summarize_text(text)
        parts.append(f"\n---\n\n## Файл: {pdf.name}\n\n")
        parts.append(summary)

    out_path = folder / OUTPUT_FILENAME
    out_path.write_text("\n".join(parts), encoding="utf-8")
    return len(pdfs), out_path


def main():
    # Iterate numeric folders at BASE_DIR
    folders = [p for p in BASE_DIR.iterdir() if p.is_dir() and p.name.isdigit()]
    folders.sort(key=lambda p: int(p.name))

    total_pdfs = 0
    written = 0

    for f in folders:
        count, out = process_folder(f)
        if count:
            total_pdfs += count
            written += 1
            print(f"Written {out} with {count} PDFs")
        else:
            print(f"No PDFs in {f}")

    print(f"Done. Processed {written} folders, {total_pdfs} PDFs total.")


if __name__ == "__main__":
    main()
