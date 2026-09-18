# Agent instructions

This repository is a sourced knowledge base about one person's career, plus the job applications built from it. Agents maintain it together with that person. The person owns every decision to send, share or publish.

- Answer briefly and clearly, in the user's language.
- Read [README.md](README.md) before editing the knowledge base or application documents. Keep the structure light and create files only when they are needed.
- Follow [docs/workflow.md](docs/workflow.md) for maintenance. After a change, run `python scripts/check_repo.py` and `git diff --check`, and check that claims still match their sources. A passing check does not mean the content is ready to publish.

## Facts and sources

- Never invent work history, education, skills, responsibilities, results, numbers or dates. Mark missing or conflicting information as open and ask the user about anything that matters.
- Keep original material in `sources/`. Do not edit a source after it is written; record corrections as a new dated source that refers to the earlier one.
- Information the user tells you is a valid source. Save what matters in a dated Markdown note and keep what the user said separate from your own interpretation.
- Link each group of facts in `knowledge/` to its sources with relative Markdown links. One source per sentence is not needed.
- Mark the user's own estimates of workload, share of the work or impact as estimates. Do not present them as measured results, and do not put exact percentages in a CV without knowing how they were calculated. Keep requirements and goals apart from achieved results.
- Keep work, studies, own projects, hobbies and voluntary roles apart. Separate the person's own implementation from AI-assisted work, team results and product scale.
- Do not store an employer's internal product names, code names or component names anywhere in the repository, including sources and commit messages. Use descriptive generic names instead and do not keep a mapping between the two.
- One knowledge base serves applications in every language. Keep official titles and degree names as they are and record translations next to them. Do not invent official translations or degree equivalences.

## Application documents

- Start every new job posting with a fit assessment: requirements, evidence found in the knowledge base, missing information and skill gaps.
- Tailor selection, emphasis and wording within what the sources support. An application document is never new evidence of a skill.
- Write documents in the language of the posting unless the user asks otherwise.
- Keep source links and internal assessments in the knowledge base and the fit assessment, not in the CV or cover letter that will be sent.
- Every CV text delivered to the user is kept as a numbered file (`cv-v1.md`, `cv-v2.md`, ...). Never edit a delivered version; feedback produces the next one.
- Generate PDFs from the Markdown source and the shared layout template. Check both the text and every rendered page before handing a PDF over.
- Keep the status, dates and notes of each application in its `tracking.md`.
- Mark an application as sent only when the user says so. Keep the exact files that were sent in `sent/` and never regenerate them.
- Preparing documents does not authorise sending applications or messages, or publishing personal information.

## Independent reviews

- Get an independent model review of a CV version when the user asks for one, following [docs/independent-reviews.md](docs/independent-reviews.md).
- Give the reviewer only the text and the boundaries it needs, never the whole knowledge base or contact details.
- Record the model that actually ran, not only the one requested, and write down why each material finding was accepted or rejected. Agreement between models does not prove a claim is true.
