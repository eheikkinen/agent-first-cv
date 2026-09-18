# Event pipeline migration

**Date:** 2026-01-11. **Source:** the person, in a conversation with the agent. Summarised by the agent.

## What the person said

- In 2023–2024 the tracking platform moved from nightly batch jobs to an event pipeline on Kafka, so that customers see shipment status changes during the day instead of the next morning.
- The person proposed the change, wrote the design document and led the technical work. A team of six took part.
- The person wrote "most of" the consumer services that turn carrier events into shipment status updates. Their own estimate is about 70 % of that code.
- The new pipeline has to make an event visible to customers within 60 seconds. "We hit that."
- The old batch jobs were switched off in spring 2024.

## Agent's notes

- 70 % is the person's estimate. It is not measured and the basis of the calculation is not known, so it does not belong in a CV as a number.
- It is unclear whether 60 seconds is a requirement or a measured result. To be clarified.
