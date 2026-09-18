# Correction: team size and latency

**Date:** 2026-01-12. **Source:** the person, answering the agent's questions. Corrects [the note of 2026-01-11](2026-01-11-event-pipeline-migration.md).

## What the person said

- The core team of the migration was four developers, not six. Two more people from operations helped with the Kafka cluster for a few weeks.
- 60 seconds is the requirement in the product specification. The person does not have a measured average or percentile. Alerts fire if events are delayed more than 60 seconds, and the person does not remember the alert firing in normal operation after launch.

## Agent's notes

- A CV can say that the pipeline was built to a 60-second requirement. It must not say that events arrive in under 60 seconds on average.
- "Rarely alerted" is the person's recollection, not monitoring data.
