"""Build a CV from the repository's small Markdown subset, entirely offline."""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import re

import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph,
)


def inline(text: str) -> str:
    """Escape input before supporting bold and explicit safe hyperlinks."""
    value = escape(text)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    return re.sub(
        r"\[([^\]]+)\]\((https://[^\s)]+|mailto:[^\s)]+|tel:[^\s)]+)\)",
        r'<link href="\2" color="#173A53">\1</link>',
        value,
    )


def pick_fonts(candidates: list[dict[str, str]]) -> dict[str, Path]:
    """Use the first font family whose files all exist, else ReportLab's bundled Vera."""
    for family in candidates:
        paths = {key: Path(value).expanduser() for key, value in family.items()}
        if all(path.is_file() for path in paths.values()):
            return paths
    bundled = Path(reportlab.__file__).parent / "fonts"
    return {"regular": bundled / "Vera.ttf", "bold": bundled / "VeraBd.ttf",
            "italic": bundled / "VeraIt.ttf", "bold_italic": bundled / "VeraBI.ttf"}


def build(source: Path, output: Path, style_path: Path, label: str | None) -> None:
    cfg = json.loads(style_path.read_text(encoding="utf-8"))
    fonts = pick_fonts(cfg["fonts"])
    for suffix, key in [("", "regular"), ("-Bold", "bold"),
                        ("-Italic", "italic"), ("-BoldItalic", "bold_italic")]:
        pdfmetrics.registerFont(TTFont(f"CV{suffix}", str(fonts[key])))
    pdfmetrics.registerFontFamily(
        "CV", normal="CV", bold="CV-Bold", italic="CV-Italic", boldItalic="CV-BoldItalic"
    )
    accent = colors.HexColor(cfg["accent"])
    muted = colors.HexColor(cfg["muted"])
    body = ParagraphStyle(
        "Body", fontName="CV", fontSize=cfg["body_size"],
        leading=cfg["body_leading"], textColor=colors.HexColor(cfg["text"]),
        spaceAfter=cfg["paragraph_space"], alignment=TA_LEFT,
        allowWidows=0, allowOrphans=0,
    )
    styles = {
        "body": body,
        "name": ParagraphStyle("Name", parent=body, fontName="CV-Bold", fontSize=30,
                               leading=34, textColor=accent, spaceAfter=5, keepWithNext=True),
        "tagline": ParagraphStyle("Tagline", parent=body, fontSize=12, leading=16,
                                  textColor=accent, spaceAfter=8, keepWithNext=True),
        "contact": ParagraphStyle("Contact", parent=body, fontSize=9.7, leading=13,
                                  textColor=muted, spaceAfter=6, keepWithNext=True),
        "section": ParagraphStyle("Section", parent=body, fontName="CV-Bold", fontSize=10,
                                  leading=13, textColor=accent, spaceBefore=cfg["section_space"],
                                  spaceAfter=7, keepWithNext=True),
        "entry": ParagraphStyle("Entry", parent=body, fontName="CV-Bold", fontSize=12,
                                leading=15, spaceBefore=5, spaceAfter=3, keepWithNext=True),
        "meta": ParagraphStyle("Meta", parent=body, fontSize=10.1, leading=13,
                               textColor=muted, spaceAfter=6, keepWithNext=True),
        "bullet": ParagraphStyle("Bullet", parent=body, leftIndent=10, firstLineIndent=0,
                                 bulletIndent=0, bulletFontName="CV", bulletFontSize=10,
                                 spaceAfter=cfg["bullet_space"]),
    }
    text = source.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", text.strip())
    name = blocks[0].removeprefix("# ").strip()
    tagline = next((b[2:].strip() for b in blocks if b.startswith("> ")), "")
    output.parent.mkdir(parents=True, exist_ok=True)
    margin = cfg["margin_mm"] * mm
    doc = BaseDocTemplate(
        str(output), pagesize=A4, leftMargin=margin, rightMargin=margin,
        topMargin=17 * mm, bottomMargin=18 * mm,
        title=" | ".join(part for part in (name, tagline) if part),
        author=name, subject="Curriculum vitae",
        creator="Local CV builder / ReportLab",
    )

    def decorate(canvas, document):
        width, height = A4
        canvas.saveState()
        canvas.setStrokeColor(accent)
        canvas.setLineWidth(1.4)
        canvas.line(margin, height - 11 * mm, margin + 28 * mm, height - 11 * mm)
        if document.page > 1:
            canvas.setFont("CV", 8.5)
            canvas.setFillColor(muted)
            canvas.drawRightString(width - margin, height - 11 * mm, name)
        canvas.setStrokeColor(colors.HexColor(cfg["rule"]))
        canvas.setLineWidth(0.4)
        canvas.line(margin, 15 * mm, width - margin, 15 * mm)
        canvas.setFont("CV", 8.5)
        canvas.setFillColor(muted)
        footer = f"DRAFT | {label}" if label else name
        canvas.drawString(margin, 10.5 * mm, footer)
        canvas.drawRightString(width - margin, 10.5 * mm, str(document.page))
        canvas.restoreState()

    frame = Frame(margin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id="CV", frames=frame, onPage=decorate))
    story = []
    in_header = True
    after_entry = False
    for block in blocks:
        if block == "<!-- pagebreak -->":
            story.append(PageBreak())
            continue
        if block.startswith("# "):
            story.append(Paragraph(inline(block[2:]), styles["name"]))
        elif block.startswith("> "):
            story.append(Paragraph(inline(block[2:]), styles["tagline"]))
        elif block.startswith("## "):
            in_header = False
            story.append(Paragraph(inline(block[3:].upper()), styles["section"]))
        elif block.startswith("### "):
            story.append(Paragraph(inline(block[4:]), styles["entry"]))
            after_entry = True
        elif block.startswith("- "):
            for item in block.split("\n- "):
                story.append(Paragraph(inline(item.removeprefix("- ")),
                                       styles["bullet"], bulletText="\u2022"))
            after_entry = False
        else:
            style = "contact" if in_header else "meta" if after_entry and " | " in block else "body"
            story.append(Paragraph(inline(" ".join(block.splitlines())), styles[style]))
            after_entry = style == "meta"
    doc.build(story)
    print(f"Created {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--style", type=Path,
                        default=Path(__file__).resolve().parents[1] / "templates/cv-style.json")
    parser.add_argument("--draft", metavar="LABEL",
                        help="mark every page as a draft, e.g. --draft 'Example Routes v2'")
    args = parser.parse_args()
    build(args.source, args.output, args.style, args.draft)
