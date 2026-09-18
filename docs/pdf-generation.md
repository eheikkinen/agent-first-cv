# PDF generation

A CV is written as Markdown and turned into a PDF locally with [build_cv.py](../scripts/build_cv.py) and the shared [layout template](../templates/cv-style.json). Nothing is sent to an online service. Text and layout stay separate, so a wording change never means fiddling with a word processor.

![CV v2 of the example application, rendered by build_cv.py](images/cv-v2-preview.png)

## Build

Requires Python 3.10+ and ReportLab (`pip install reportlab`).

```sh
python scripts/build_cv.py \
  applications/2026-01-15-example-routes-senior-platform-engineer/cv-v2.md \
  applications/2026-01-15-example-routes-senior-platform-engineer/output/cv-v2.pdf \
  --draft "Example Routes - Senior Platform Engineer"
```

`--draft LABEL` puts a draft mark and the label in the footer of every page. Leave it out for the version that will be sent. `output/` folders are ignored by Git; files that were actually sent are kept in `sent/`.

The template uses the first font family whose files exist: Calibri on Windows, then Carlito (metric-compatible, `fonts-crosextra-carlito` on Debian and Ubuntu), then the Vera fonts bundled with ReportLab. Used glyphs are embedded in the PDF.

## Supported Markdown

A deliberately small subset, not a general Markdown renderer:

| Markdown | Becomes |
| --- | --- |
| `# Name` | Name at the top |
| `> Title` | Professional title under the name |
| Paragraphs before the first `##` | Contact lines |
| `## Section` | Section heading |
| `### Employer or project` | Entry heading |
| `**Title** \| dates` right after an entry | Role and dates line |
| `- item` | Bullet |
| `**bold**`, `[text](https://...)`, `mailto:` and `tel:` links | Inline formatting and links |
| `<!-- pagebreak -->` | Page break |

## Checking the result

Look at every page as an image: line breaks, margins, page breaks and overlaps. Then check the text layer, for example with `pdftotext -layout`, because recruiting systems read the text, not the picture. Check that links point where they should and that the fonts are embedded (`pdffonts`).
