# CV v1 review request

Review the CV text below. You have no tools and no other files; judge the text only. Reply in English. Give at most five material findings, most important first, each with a concrete replacement wording where useful. End with a one-line verdict on whether the text is ready for the candidate's own feedback. Do not rewrite the whole CV.

## Target role

Senior Platform Engineer at a route planning software company. The platform team owns CI/CD, Kubernetes and the tooling around them, makes services observable (metrics, logs, traces) and helps about 60 product engineers adopt AI coding agents safely. Terraform is asked for.

## Boundaries the text must stay within

Confirmed by the candidate:

- Software Engineer at the current employer from March 2018, Senior Software Engineer from 2021.
- Proposed, designed and technically led a 2023–2024 migration from nightly batch jobs to a Kafka event pipeline, with a core team of four. Wrote most of the consumer services; their own estimate of their share is not measured.
- 60 seconds is the product requirement for event delivery. There is no measured average or percentile.
- Built an internal CLI for local development environments. The candidate says most of the backend team uses it; usage is not measured.
- Wrote an AGENTS.md for the main repository; two other backend repositories copied it. Added a CI step that posts a model-generated summary of each pull request as a comment for reviewers. Gave one internal talk to about 20 colleagues.
- Set up Grafana dashboards, alert rules and Loki logging for the pipeline. No distributed tracing.
- Has read and made small changes to Terraform modules but has not designed with Terraform.
- Own project: a public weather app. The candidate wrote the data caching service; an AI agent wrote the React user interface.

Nothing about reduced incidents, team-wide adoption numbers or measured latency is confirmed.

## What to assess

1. Claims that go beyond the boundaries above.
2. Fit for the target role.
3. Clarity and concision; generic phrases that say nothing.

## CV text (contact details omitted)

# Alex Example

> Senior Software Engineer | Backend and Platform

## Profile

Senior software engineer with eight years of backend development on a production logistics platform. Passionate about developer experience, event-driven architecture and leveraging AI to empower engineering teams. Proven track record of delivering complex migrations and reducing incidents.

## Technical skills

**Backend:** Python, Go, PostgreSQL, Kafka.

**Platform:** Kubernetes, Helm, Docker, Grafana, Loki.

**AI agents:** Claude Code, shared AGENTS.md instructions, model-generated pull request summaries in CI.

## Experience

### Example Freight Oy

**Senior Software Engineer** | 2018 - Present | Tampere

- Led the migration of the shipment tracking platform from nightly batch jobs to a Kafka event pipeline, delivering real-time updates in under 60 seconds.
- Built an internal CLI that starts local development environments with the right service versions, adopted by the backend team.
- Introduced shared agent instructions and AI pull request summaries across the backend repositories.
- Set up Grafana dashboards and alerting for the event pipeline.
- Participate in the on-call rotation.

### Example Web Oy

**Software Developer** | Aug 2015 - Feb 2018

- Developed customer websites using PHP and JavaScript.
- Worked closely with designers and customers to deliver high-quality web solutions.

## Own projects

### Harbour Weather

Wind and sea-level forecasts for small-boat harbours, built with TypeScript, React, Node.js and Docker.

## Education

**Bachelor of Engineering, Software Engineering** | Example University of Applied Sciences | 2011 - 2015

## Languages

**Finnish:** native. **English:** fluent.
