# Projects

What the person built, what their own part was and what is known about the result. Work and own projects are kept apart.

## Work at Example Freight

### Event pipeline migration

**When:** 2023–2024. **Role:** proposed the change, wrote the design document and led the technical work.

- Moved the tracking platform from nightly batch jobs to an event pipeline on Kafka, so that customers see shipment status changes during the day instead of the next morning.
- Core team of four developers; two people from operations helped with the Kafka cluster for a few weeks.
- Wrote most of the consumer services that turn carrier events into status updates. The person estimates their share at about 70 %; this is an unmeasured estimate and is not used as a number in CVs.
- Built to a product requirement that events reach customers within 60 seconds. There is no measured average or percentile; the person recalls the delay alert rarely firing after launch.
- The old batch jobs were switched off in spring 2024.
- Set up the Grafana dashboards and alert rules for the pipeline in 2024. Logs go to Loki; there is no distributed tracing.

[Source](../sources/2026-01-11-event-pipeline-migration.md), [correction to team size and latency](../sources/2026-01-12-correction-team-size-and-latency.md), [observability](../sources/2026-01-16-platform-role-clarifications.md).

### Local environment CLI

An internal command-line tool that starts a developer's local environment with the right service versions. The person describes it as used by most of the backend team; the number of users is not known.

[Source](../sources/2026-01-10-career-interview.md).

### AI adoption in the backend team

- Uses Claude Code daily for implementation and for reading unfamiliar code, and reviews every change line by line before opening a pull request.
- Wrote an `AGENTS.md` for the main repository in 2025 with build commands, test conventions and off-limits directories. Two other backend repositories copied it.
- Added a CI step that writes a model-generated summary of each pull request as a comment for reviewers. Nothing is merged automatically. The number of summarised pull requests is not known.
- Gave an internal talk, "Agents in our codebase", to about 20 colleagues (estimate) in autumn 2025.

[Source](../sources/2026-01-11-ai-in-daily-work.md).

## Own projects

### Harbour Weather

A spare-time web app showing wind and sea-level forecasts for small-boat harbours on the Finnish coast, built on open weather and sea-level data.

- TypeScript and React front end, a Node.js caching service, Docker Compose and nginx on a rented virtual server.
- The person wrote the data caching logic; an AI agent wrote the user interface.
- Public site; a few dozen visitors a week in summer by the person's estimate.

[Source](../sources/2026-01-11-own-project-harbour-weather.md).
