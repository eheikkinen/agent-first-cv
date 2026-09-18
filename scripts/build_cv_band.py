"""Render a CV Markdown file in the "Modern band" layout and print it to PDF with Chromium.

The layout has a coloured header band with contact details and a photo or initials.
Two variants are available:

  --pages 2  Page 1: profile and professional experience in full width.
             Page 2: projects and earlier experience beside a side panel.
  --pages 1  Everything on one page: main column beside the side panel.

Any Chromium-based browser prints the page: Chrome, Edge, Chromium or Playwright's
headless shell. Set CHROME to its path if it is not found automatically. Python needs
only the standard library. The Google Fonts stylesheet is the only network request.
"""

from __future__ import annotations

import argparse
import base64
from html import escape
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ACCENT = "#2451c7"
BAND = "#eaf0f7"

# Section names in the CV Markdown, lower case, mapped to the layout's slots.
SECTIONS = {
    "profile": "profile",
    "professional experience": "work", "experience": "work",
    "independent projects": "projects", "own projects": "projects", "projects": "projects",
    "earlier experience": "earlier",
    "technical skills": "skills", "skills": "skills",
    "education": "education",
    "languages": "languages",
}

ICONS = {
    "location": '<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"></path><circle cx="12" cy="10" r="2.5"></circle>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"></rect><path d="M3 7l9 6 9-6"></path>',
    "phone": '<rect x="7" y="2" width="10" height="20" rx="2"></rect><path d="M11 18h2"></path>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"></path><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"></path>',
    "github": '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"></path>',
}

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; background: #fff; font-family: "DM Sans", system-ui, sans-serif; color: #14202e;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: inherit; text-decoration: none; }
ul { margin: 0; padding: 0 0 0 14px; }
li { margin: 0 0 3px 0; padding-left: 3px; text-wrap: pretty; }
li::marker { color: ACCENT; }
p { margin: 0; text-wrap: pretty; }
.page { width: 794px; height: 1122px; overflow: hidden; display: flex; flex-direction: column;
        font-size: 13px; line-height: 1.42; break-after: page; }
.page:last-of-type { break-after: auto; }
h1, h2, h3, .tagline { font-family: "Space Grotesk", system-ui, sans-serif; }
header { display: flex; gap: 28px; align-items: center; padding: 40px 60px 30px; background: BAND; }
h1 { margin: 0; font-size: 38px; line-height: 1; font-weight: 700; letter-spacing: -0.025em; }
.tagline { font-size: 16px; font-weight: 500; color: ACCENT; }
.contacts { display: flex; flex-wrap: wrap; gap: 6px 18px; margin-top: 8px; font-size: 12.5px; color: #3a4757; }
.contacts > * { display: flex; align-items: center; gap: 6px; }
.photo { width: 112px; height: 112px; flex-shrink: 0; object-fit: cover; object-position: center top;
         border-radius: 50%; border: 4px solid #fff; background: #fff; }
.initials { width: 112px; height: 112px; flex-shrink: 0; border-radius: 50%; border: 4px solid #fff;
            background: ACCENT; color: #fff; display: flex; align-items: center; justify-content: center;
            font-family: "Space Grotesk", system-ui, sans-serif; font-size: 40px; font-weight: 600;
            letter-spacing: -0.02em; }
h2 { margin: 0; display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 600;
     letter-spacing: 0.08em; text-transform: uppercase; color: ACCENT; }
h2 .bar { width: 18px; height: 3px; background: ACCENT; border-radius: 2px; }
h3 { margin: 0; font-weight: 600; }
.sub { font-weight: 500; color: #3a4757; }
.pill { padding: 3px 10px; border-radius: 999px; background: BAND; font-size: 12px; font-weight: 500;
        white-space: nowrap; }
.entry-head { display: flex; justify-content: space-between; align-items: center; gap: 16px; }
.role-line { display: flex; justify-content: space-between; align-items: center; gap: 16px;
             font-weight: 500; color: #3a4757; }
.body { flex-grow: 1; display: flex; flex-direction: column; gap: 22px; padding: 26px 60px 40px; }
.p2 .body { padding-top: 48px; }
section { display: flex; flex-direction: column; gap: 9px; }
.entry { display: flex; flex-direction: column; gap: 4px; }
.entry + .entry { margin-top: 4px; }
.intro { font-style: italic; color: #3a4757; }
.columns { display: grid; grid-template-columns: minmax(0, 1fr) 236px; column-gap: 26px; align-items: start; }
.column { display: flex; flex-direction: column; gap: 22px; }
aside { display: flex; flex-direction: column; gap: 20px; padding: 20px 18px; border-radius: 10px;
        background: BAND; font-size: 12.5px; }
aside h2 { display: block; }
aside section { gap: 6px; }
aside .item { display: flex; flex-direction: column; gap: 1px; }
.b { font-weight: 600; }
footer { margin-top: auto; display: flex; justify-content: space-between; font-size: 12px; color: #5b6878; }
.inline-link { color: ACCENT; }
""".replace("ACCENT", ACCENT).replace("BAND", BAND)

FONTS = ("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=DM+Sans:"
         "ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap")

MEASURE = """<script>
document.body.dataset.overflow = [...document.querySelectorAll('.page')]
  .map(page => page.scrollHeight - page.clientHeight).join(',');
</script>"""


def inline(text: str) -> str:
    """Escape text, then support **bold** and explicit https/mailto/tel links."""
    value = escape(text, quote=False)
    value = re.sub(r"\*\*(.+?)\*\*", r'<span class="b">\1</span>', value)
    return re.sub(r"\[([^\]]+)\]\(((?:https://|mailto:|tel:)[^\s)]+)\)",
                  r'<a class="inline-link" href="\2">\1</a>', value)


def dashes(text: str) -> str:
    return re.sub(r"(\w) - (\w)", "\\1 \u2013 \\2", text)


def icon(name: str) -> str:
    return ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f"{ICONS[name]}</svg>")


def parse(source: Path) -> tuple[dict, dict[str, list[str]]]:
    """Split the Markdown into header fields and layout slots of blank-line separated blocks."""
    blocks = re.split(r"\n\s*\n", source.read_text(encoding="utf-8").strip())
    head = {"name": "", "tagline": "", "contacts": []}
    slots: dict[str, list[str]] = {}
    current = None
    for block in blocks:
        block = block.strip()
        if block.startswith("## "):
            title = block[3:].strip().lower()
            if title not in SECTIONS:
                raise SystemExit(f"Unknown section '## {block[3:].strip()}'. Known: {', '.join(SECTIONS)}")
            current = SECTIONS[title]
            slots.setdefault(current, [])
        elif current is not None:
            slots[current].append(block)
        elif block.startswith("# "):
            head["name"] = block[2:].strip()
        elif block.startswith("> "):
            head["tagline"] = block[2:].strip()
        elif block != "<!-- pagebreak -->":
            head["contacts"] += [part.strip() for part in " ".join(block.splitlines()).split(" | ")]
    return head, slots


def entries(blocks: list[str]) -> tuple[list[str], list[dict]]:
    """Group blocks under ### headings; blocks before the first heading are an intro."""
    intro, result = [], []
    for block in blocks:
        if block.startswith("### "):
            result.append({"title": block[4:].strip(), "meta": [], "text": [], "bullets": []})
        elif not result:
            intro.append(block)
        elif block.startswith("- "):
            result[-1]["bullets"] += [item.removeprefix("- ").strip() for item in block.split("\n- ")]
        elif block.startswith("**") and " | " in block and not result[-1]["text"]:
            result[-1]["meta"].append(block)
        else:
            result[-1]["text"].append(" ".join(block.splitlines()))
    return intro, result


def split_meta(meta: str) -> tuple[str, str, str]:
    """'**Role** | Sep 2015 - Present | Helsinki' -> role, dates, the rest."""
    parts = [part.strip() for part in meta.split(" | ")]
    role = parts[0].strip("*")
    dates = next((p for p in parts[1:] if re.search(r"\d{4}", p)), "")
    rest = " · ".join(p for p in parts[1:] if p != dates)
    return role, dashes(dates), rest


def heading(title: str) -> str:
    return f'<h2><span class="bar"></span>{escape(title)}</h2>'


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ul>" if items else ""


def paragraphs(texts: list[str], margin: str = "0") -> str:
    return "".join(f'<p style="margin:{margin}">{inline(t)}</p>' for t in texts)


def job(entry: dict, size: int) -> str:
    """Employer entry: latest role as the title, employer below, dates as a pill.
    Earlier roles at the same employer follow as smaller lines."""
    if not entry["meta"]:
        return project(entry)
    role, dates, place = split_meta(entry["meta"][0])
    employer = " · ".join(p for p in (inline(entry["title"]), escape(place)) if p)
    earlier_roles = ""
    for meta in entry["meta"][1:]:
        other, other_dates, _ = split_meta(meta)
        earlier_roles += f'<div class="role-line"><span>{escape(other)}</span><span class="pill">{escape(other_dates)}</span></div>'
    return (f'<div class="entry"><div class="entry-head"><div style="display:flex;flex-direction:column;gap:1px">'
            f'<h3 style="font-size:{size}px">{escape(role)}</h3><span class="sub">{employer}</span></div>'
            f'<span class="pill">{escape(dates)}</span></div>{earlier_roles}'
            f'{paragraphs(entry["text"], "2px 0")}{bullets(entry["bullets"])}</div>')


def project(entry: dict) -> str:
    name, _, subtitle = entry["title"].partition(" | ")
    sub = f'<span class="sub">{inline(subtitle)}</span>' if subtitle else ""
    return (f'<div class="entry"><h3 style="font-size:16px">{inline(name)}</h3>{sub}'
            f'{paragraphs(entry["text"], "2px 0 0")}{bullets(entry["bullets"])}</div>')


def contact_html(items: list[str]) -> str:
    html = []
    for item in items:
        link = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", item)
        if not link:
            html.append(f"<span>{icon('location')}{escape(item)}</span>")
            continue
        label, href = link.groups()
        kind = ("mail" if href.startswith("mailto:") else "phone" if href.startswith("tel:")
                else "github" if "github.com" in href else "link")
        html.append(f'<a href="{escape(href)}">{icon(kind)}{escape(label)}</a>')
    return "".join(html)


def portrait(name: str, photo: Path | None) -> str:
    if photo:
        kind = "jpeg" if photo.suffix.lower() in (".jpg", ".jpeg") else "png"
        data = base64.b64encode(photo.read_bytes()).decode("ascii")
        return f'<img class="photo" src="data:image/{kind};base64,{data}" alt="{escape(name)}">'
    initials = "".join(word[0] for word in name.split()[:2]).upper()
    return f'<div class="initials" aria-hidden="true">{escape(initials)}</div>'


def side_panel(slots: dict[str, list[str]]) -> str:
    skills = []
    for block in slots.get("skills", []):
        match = re.fullmatch(r"\*\*(.+?):\*\*\s*(.+)", " ".join(block.splitlines()))
        if match:
            skills.append(f'<div class="item"><span class="b">{escape(match.group(1))}</span>'
                          f"<span>{inline(match.group(2))}</span></div>")
    intro, education = entries(slots.get("education", []))
    edu = []
    for block in intro:
        parts = [p.strip() for p in " ".join(block.splitlines()).split(" | ")]
        edu.append(f'<span class="b">{inline(parts[0])}</span>'
                   + "".join(f"<span>{inline(dashes(p))}</span>" for p in parts[1:]))
    for entry in education:
        degree, dates, _ = split_meta(entry["meta"][0]) if entry["meta"] else ("", "", "")
        edu.append(f'<span class="b">{escape(degree)}</span><span>{inline(entry["title"])} · {escape(dates)}</span>'
                   + "".join(f"<span>{inline(t)}</span>" for t in entry["text"]))
    languages = []
    for block in slots.get("languages", []):
        for match in re.finditer(r"\*\*(.+?)\*\*\s*(.+?)(?=\s*\*\*|$)", " ".join(block.splitlines())):
            languages.append(f'<span><span class="b">{escape(match.group(1))}</span> {inline(match.group(2))}</span>')
    parts = [("Technical skills", skills), ("Education", edu), ("Languages", languages)]
    return "<aside>" + "".join(f"<section><h2>{title}</h2>{''.join(items)}</section>"
                               for title, items in parts if items) + "</aside>"


def render(source: Path, photo: Path | None, pages: int) -> str:
    head, slots = parse(source)
    name = escape(head["name"])
    header = (f'<header><div style="flex-grow:1;display:flex;flex-direction:column;gap:6px">'
              f'<h1>{name}</h1><div class="tagline">{inline(head["tagline"].replace(" | ", " · "))}</div>'
              f'<div class="contacts">{contact_html(head["contacts"])}</div></div>'
              f'{portrait(head["name"], photo)}</header>')
    profile = "".join(f'<p style="font-size:13.5px">{inline(" ".join(b.splitlines()))}</p>'
                      for b in slots.get("profile", []))
    _, work = entries(slots.get("work", []))
    intro, projects = entries(slots.get("projects", []))
    _, earlier = entries(slots.get("earlier", []))

    def section(title: str, html: str) -> str:
        return f"<section>{heading(title)}{html}</section>" if html else ""

    work_html = "".join(job(e, 17 if pages == 2 else 16) for e in work)
    projects_html = ("".join(f'<p class="intro">{inline(t)}</p>' for t in intro)
                     + "".join(project(e) for e in projects))
    earlier_html = "".join(job(e, 15) for e in earlier)

    def footer(number: int) -> str:
        return f"<footer><span>{name} · CV</span><span>{number} / {pages}</span></footer>"

    if pages == 1:
        body = (f'<div class="columns"><div class="column">{section("Profile", profile)}'
                f'{section("Experience", work_html)}{section("Own projects", projects_html)}'
                f'{section("Earlier experience", earlier_html)}</div>{side_panel(slots)}</div>')
        html = f'<div class="page p1">{header}<div class="body">{body}{footer(1)}</div></div>'
    else:
        html = (f'<div class="page p1">{header}<div class="body">{section("Profile", profile)}'
                f'{section("Professional experience", work_html)}{footer(1)}</div></div>'
                f'<div class="page p2"><div class="body"><div class="columns"><div class="column">'
                f'{section("Independent projects", projects_html)}{section("Earlier experience", earlier_html)}'
                f'</div>{side_panel(slots)}</div>{footer(2)}</div></div>')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{name} | CV</title>'
            f'<link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head>'
            f"<body>{html}{MEASURE}</body></html>")


def find_chrome() -> Path:
    """CHROME, then common browser names on PATH, then usual install and Playwright locations."""
    if os.environ.get("CHROME"):
        chrome = Path(os.environ["CHROME"])
        if not chrome.is_file():
            raise SystemExit(f"CHROME points to a missing file: {chrome}")
        return chrome
    for name in ("chrome-headless-shell", "chromium", "chromium-browser", "google-chrome",
                 "google-chrome-stable", "chrome", "msedge", "microsoft-edge"):
        found = shutil.which(name)
        if found:
            return Path(found)
    home = Path.home()
    fixed = [
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    ]
    for path in fixed:
        if path.is_file():
            return path
    for cache in (home / "AppData/Local/ms-playwright", home / ".cache/ms-playwright",
                  home / "Library/Caches/ms-playwright"):
        found = sorted(cache.glob("chromium_headless_shell-*/*/chrome-headless-shell*"))
        found = [p for p in found if p.is_file()]
        if found:
            return found[-1]
    raise SystemExit("No Chromium-based browser found. Install Chrome or Chromium, run "
                     "'npx playwright install chromium-headless-shell', or set CHROME to a browser path.")


def overflow(chrome: Path, html_path: Path, profile: str) -> list[int]:
    """Pixels by which each page's content exceeds the page, measured in the browser."""
    dom = subprocess.run([str(chrome), "--headless", "--disable-gpu", f"--user-data-dir={profile}",
                          "--virtual-time-budget=10000", "--dump-dom", html_path.resolve().as_uri()],
                         check=True, capture_output=True, text=True, encoding="utf-8").stdout
    return [int(v) for v in re.search(r'data-overflow="([^"]*)"', dom).group(1).split(",")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path, help="PDF path; the HTML is written next to it")
    parser.add_argument("--pages", type=int, choices=(1, 2), default=2)
    parser.add_argument("--photo", type=Path, help="PNG or JPEG portrait; initials are shown without one")
    args = parser.parse_args()
    html = render(args.source, args.photo, args.pages)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    html_path = args.output.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    chrome = find_chrome()
    with tempfile.TemporaryDirectory() as profile:
        excess = overflow(chrome, html_path, profile)
        if any(px > 0 for px in excess):
            raise SystemExit(f"Content does not fit: overflow per page {excess} px. Shorten the text.")
        subprocess.run([str(chrome), "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--user-data-dir={profile}", "--virtual-time-budget=10000",
                        f"--print-to-pdf={args.output.resolve()}", html_path.resolve().as_uri()],
                       check=True, capture_output=True)
    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
