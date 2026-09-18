# Fit assessment — Example Routes, Senior Platform Engineer

Written 2026-01-15 from the knowledge base and the [posting](job.md); updated 2026-01-16 with the person's [answers to open questions](../../sources/2026-01-16-platform-role-clarifications.md). This is the agent's assessment, not a recruiter's decision.

## Conclusion

Worth applying. The role matches the person's [direction](../../knowledge/profile.md#direction): developer tooling and AI adoption on top of solid backend work. The strongest evidence is the event pipeline migration, the internal CLI and the team's shared agent instructions. Terraform is a real gap and the CV should not hide it; tracing is also missing.

## Requirements and evidence

| Posting asks for | Evidence in the knowledge base | Assessment |
| --- | --- | --- |
| Backend or platform engineering in production | Tracking platform backend since 2018, on-call rotation. [Experience](../../knowledge/experience.md#example-freight-oy) | Strong. |
| Kubernetes | Platform runs on Kubernetes; maintains Helm charts with two colleagues. [Skills](../../knowledge/skills.md) | Good for application-side work. Cluster administration not shown. |
| Event-driven systems | Led the Kafka migration and wrote most of the consumers. [Project](../../knowledge/projects.md#event-pipeline-migration) | Strong and specific. The 60-second figure is a requirement, not a measurement. |
| Observability | Grafana dashboards, alert rules and Loki for the event pipeline. [Project](../../knowledge/projects.md#event-pipeline-migration) | Good for metrics and logs. No tracing. |
| Infrastructure as code, Terraform | Reads and makes small changes to team modules; has not designed with Terraform. [Clarification](../../sources/2026-01-16-platform-role-clarifications.md) | Gap. Leave out of skills; be ready to discuss in the interview. |
| Developer experience | Local environment CLI used by most of the backend team (person's description). [Project](../../knowledge/projects.md#local-environment-cli) | Good. Usage not measured. |
| Helping teams adopt AI agents | `AGENTS.md` copied by two other repositories, PR summaries in CI, internal talk. [Project](../../knowledge/projects.md#ai-adoption-in-the-backend-team) | Good, at team level. No organisation-wide programme. |
| Go (nice to have) | Some Go in the tracking platform; extent open. | Mention in skills without emphasis. |

## Evidence to lead with

1. Event pipeline migration: own proposal, design and technical lead.
2. Developer tooling: the local environment CLI.
3. AI adoption: shared agent instructions and PR summaries, with human review.
4. Observability of the pipeline: dashboards and alerts.

## Open questions

- Resolved 2026-01-16: Terraform, Helm and observability tooling.
- Still open: the extent of the Go work and the exact promotion month. Neither blocks the CV.
