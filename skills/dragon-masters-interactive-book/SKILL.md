---
name: dragon-masters-interactive-book
description: Create or revise an illustrated browser-based interactive book from user-supplied story sources, including evidence-grounded scene planning, consistent character art, state-specific illustrations, narrative gestures, bilingual text, original music cues, persistent progress, and quality checks. Use when the user requests an interactive reading experience, not an ordinary workbook or a finished third-party book download.
---

# Dragon Masters Interactive Book

Produce a continuous illustrated reading experience whose actions change the story scene visibly. This public candidate is self-contained: do not assume access to a particular author's private folders, notes, images or conversation history.

## Start

Read [workflow.md](references/workflow.md). Establish source, audience, language, platform, visual direction, output directory and permitted use. Keep source facts separate from teaching adaptations and unknowns. If a source is unavailable, pause only its dependent narrative work; use the included original example to explain the mechanics, not to invent the missing book.

Use [prompts.md](references/prompts.md) for runnable prompts at each stage. Confirm a short scene plan and character sheet before expensive full-book generation. The user's explicit plan-only/review gates remain controlling.

## Choose the work

- For a user-supplied *Rise of the Earth Dragon*, read [rise-of-the-earth-dragon.md](references/rise-of-the-earth-dragon.md). It is a source-required production profile, not an embedded book. Follow the supplied story rather than replacing it with the demo.

- Story planning: evidence table, entry/action/result/exit and adjacent-scene continuity in workflow.md.
- Images: read [art-direction.md](references/art-direction.md); lock character identity, perspective and light state; generate original compositions with permitted references; inspect every result. Never use a failed image as the next identity anchor.
- Music: read [music.md](references/music.md). Use event-based moods, not one flat loop for the whole story. Local procedural generator is included; service-based music is optional and requires the user's permitted workflow.
- Interaction/animation: read [interaction.md](references/interaction.md). Use an action because it matches a story verb. Remove arbitrary swipes instead of making instructions longer.
- Fixed-track sprite movement: use `assets/starter/track-flight.js` with a clean background and independently created sprite; instructions in interaction.md. It includes fast-input projection and frame-coalesced rendering, not free roaming.
- Implementation: read [data-contract.md](references/data-contract.md); copy starter with `scripts/new_project.py` to a NEW directory. Edit story.json, regenerate story.js with `scripts/sync_story.py`, replace art/audio and validate. The three-scene story is a demonstration, not a fixed chapter count.
- Repairs/release: read [qa.md](references/qa.md). Use visible behavior plus static checks; don't equate a successful click or image generation with acceptance.

## Non-negotiable invariants

1. Preserve source order and reveal boundaries; don't make a canonical accident the reader's fault or expose later abilities early.
2. Show the destination before asking for a destination-specific action. Carry clothing, props, dust, light and knowledge across scenes.
3. Idle/drag/placed representations are one object. Don't overlay a draggable duplicate on a baked-in object. Hit regions follow the displayed image rectangle, not the entire browser.
4. Show story dialogue before the question; hide answer-bearing dialogue and captions while Quiz is active. Prefer evidence/application questions, not copying adjacent text. Wrong answers receive hints; do not permanently lock the story.
5. Language switches, rendering and refresh must not change story facts. Save committed outcomes, not half-finished gestures. Use stable IDs, version the schema and handle malformed storage.
6. Cancel gesture/timer/image work on navigation, blur or reduced-motion changes as needed; stale callbacks cannot advance a different scene. Decode new art before showing its controls.
7. Music starts after user action, has persistent mute, crossfades on meaningful events and pauses when hidden/closed. Music is never required to understand the plot.
8. Keep desktop reading comfortable, reading text expandable, controls keyboard-reachable and motion reducible. Discuss mobile support separately rather than claiming it from responsive CSS.
9. Do not send user sources/assets to services without the required permission, put credentials into files, or publish automatically. Source possession is not a distribution license.

## Deliver

Hand off runnable HTML, local runtime assets, editable scene data, source/character/scene records, prompt set, audio provenance and QA results. Explain tools/dependencies, paid optional steps and human decisions. Preserve the user's existing work and keep public/private deliverables separate. Never claim a new-user forward test, classroom outcome or publication that was not performed.
