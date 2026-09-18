"""Check repository Markdown links and basic text integrity, without network access."""

from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>\n]+>|[^)\n]+)\)")


def prose(text):
    """Exclude fenced code examples while preserving line numbers."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield number, line


def heading_ids(text):
    """GitHub-style slugs for the plain Markdown headings used in this repo."""
    result = set()
    for _, line in prose(text):
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        label = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", match.group(1))
        label = re.sub(r"<[^>]*>", "", label).lower()
        slug = re.sub(r"[^\w\-\s]", "", label).replace(" ", "-")
        candidate = slug
        suffix = 0
        while candidate in result:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        result.add(candidate)
    result.update(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    return result


def main():
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "*.md"],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout.decode("utf-8").split("\0")
    files = sorted({ROOT / name for name in listed if name})
    errors = []
    external = []
    checked = 0
    contents = {}
    for path in files:
        try:
            contents[path.resolve()] = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: unreadable UTF-8: {exc}")

    for path, text in contents.items():
        relative = path.relative_to(ROOT)
        for number, line in enumerate(text.splitlines(), 1):
            if "\ufffd" in line or re.match(r"^(<{7}|={7}|>{7})(?:\s|$)", line):
                errors.append(f"{relative}:{number}: encoding error or merge marker")
        for number, line in prose(text):
            for match in LINK.finditer(line):
                href = match.group(1).strip().strip("<>")
                if re.match(r"^[A-Za-z]:[/\\]", href) or href.startswith(("/", "file:")):
                    external.append(f"{relative}:{number}")
                    if relative.parts[0] != "sources":
                        errors.append(f"{relative}:{number}: machine-specific link outside historical sources")
                    continue
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                if not target.is_relative_to(ROOT):
                    errors.append(f"{relative}:{number}: link escapes repository: {href}")
                    continue
                if not target.exists():
                    errors.append(f"{relative}:{number}: missing target: {href}")
                    continue
                checked += 1
                if url.fragment and target.suffix.lower() == ".md":
                    target_text = contents.get(target)
                    if target_text is None:
                        target_text = target.read_text(encoding="utf-8-sig")
                    if unquote(url.fragment) not in heading_ids(target_text):
                        errors.append(f"{relative}:{number}: missing heading: {href}")

    for error in errors:
        print(f"ERROR {error}")
    print(f"Checked {len(files)} Markdown files and {checked} repository links.")
    print(f"Historical machine-specific source links: {len(external)} (not portable; not checked).")
    print("External web URLs and publication suitability are not checked.")
    print("PASS" if not errors else f"FAIL: {len(errors)} issue(s)")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
