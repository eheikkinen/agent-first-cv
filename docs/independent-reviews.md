# Independent model reviews

The agent that writes a CV is a poor judge of it: it has read every source and fills gaps without noticing. A second model that sees only the finished text catches claims the text does not support, vague wording and a poor fit for the role.

## Running a review

1. **Write the request as a file** in the application's `reviews/` folder, for example `review-v1-request.md`. It contains:
   - the target role in two or three sentences;
   - the boundaries the text must stay within: what is confirmed, what is an estimate and what must not be implied;
   - what to assess and how much feedback is wanted, for example "at most five material findings";
   - the CV text without contact details.
2. **Run the reviewer without tools or files.** It gets the request and nothing else, so it cannot read the knowledge base and cannot change anything. With the Claude CLI, for example:

   ```sh
   claude -p --model <model> --tools= --no-session-persistence --output-format json \
     < applications/<folder>/reviews/review-v1-request.md \
     > applications/<folder>/reviews/review-v1-response.json
   ```

3. **Record the model that actually ran.** Take it from the response metadata, not from the command line. A run that failed or hit a quota is recorded as failed, not as a review.
4. **Write a readable review** (`review-v1.md`) and a **resolution summary** that lists every material finding as accepted, changed or rejected, with the reason.
5. **Deliver the next CV version** as a new file. The reviewed version stays unchanged.

## Principles

- A reviewer's suggestion is not a source. If it proposes a fact, a number or a technology that is not in the knowledge base, reject it or ask the user.
- Agreement between two models does not make a claim true; only a source does.
- Reviews are optional. Run one when the user asks for it, and stop when the user is happy with the text.
