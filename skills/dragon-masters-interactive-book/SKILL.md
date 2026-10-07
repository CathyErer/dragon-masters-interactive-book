---
name: dragon-masters-interactive-book
description: Build, revise, or audit a complete Dragon Masters Book 1 browser interactive book from a user-supplied Rise of the Earth Dragon source. Includes full-book evidence planning, original consistent art, narrative actions, chapter transitions, bilingual text, event-based music, progress, quizzes and optional retells. This Skill targets Book 1 only; internal test fixtures are not user-facing story modes.
metadata:
  version: "0.3.0"
---

# Dragon Masters Interactive Book

Deliver the requested **whole source story**, with editable production records and a runnable desktop book. Read the supplied book; never use memory, this profile, or generated pictures as proof of its contents. This public Skill needs no private notes, author-specific paths, prior chats or private book archive.

## Start DM1 production

1. Read [workflow.md](references/workflow.md). Establish source coverage, intended use, reader level, language, desktop size and output directory. Follow the user's existing approvals. Ask only for missing decisions that block the current stage.
2. For *Rise of the Earth Dragon*, read [the Book 1 profile](references/rise-of-the-earth-dragon.md) and [chapter checkpoints](references/dm1-chapter-checkpoints.md). This is a 16-chapter production target to verify against the supplied edition, not permission to fabricate missing chapters. Do not use this Skill to produce other books or original stories; they require a separately scoped workflow.
3. Run `python3 scripts/new_project.py --destination NEW_DIR`. This creates the DM1 planning workspace, 16 blank chapter records and a content-empty engine skeleton under `engine-reference/`. Fill the records; build actual runtime files under `book/` after source and sample review. There is no original-story mode or demo-launch option.
4. Report source gaps and the next concrete deliverable. With only one chapter, produce only that chapter's plan/sample and label full-book work incomplete. With no source, prepare the input checklist; do not turn checkpoints into invented book content.

## Complete the production stages

Use [production-records.md](references/production-records.md) for exact files and [prompts.md](references/prompts.md) for stage-specific prompts.

- **Read and plan:** chapter/page evidence → required events → ordered scene IDs → entry/action/result/exit → adjacent-state continuity. Preserve intermediate locations, clues, participants and final unresolved questions. Short adapted dialogue must not replace the source or become a wall of text.
- **Lock visual identity:** [art-direction.md](references/art-direction.md). Verify character features from permitted references; create an approved identity sheet, scene cameras, before/after states and transparent props. Record missing evidence. Review a representative sample before expensive full-book assets unless that scope is already approved.
- **Generate and inspect:** use the available image tool/artist with the actual identity references, exact prompts and state constraints. Inspect each result for identity, scale, light, duplicate props and premature reveals. A placeholder, prompt or successful API call is not a finished illustration.
- **Build scene actions:** [interaction.md](references/interaction.md), [data-contract.md](references/data-contract.md). The engine supports observe, drag, hold, trace, advance and integrated track sprites. Many scenes may belong to a chapter; place its Story Check at the source-derived checkpoint, not automatically after every gesture. Extend the engine where the plan requires a new mechanic; do not silently substitute repeated clicks or a demo action.
- **Score events:** [music.md](references/music.md). Use event-based original/appropriately licensed instrumental cues, local playback, persistent mute and gentle changes. No character speech by default. Procedural audio is a draft option; verify listening quality separately.
- **Connect the whole book:** physical-book opening, desktop spread, English/bilingual switching, sequential locations, independent save ID, evidence Journal and optional retells. Implement and test multi-stage chapters, ending identity and closing; a chapter Quiz need not be the chapter's last event.
- **Verify and repair:** [qa.md](references/qa.md). Run both validators, actual browser gestures and continuous whole-book routes. Compare the rendered story with source evidence. Work on concrete failures; avoid changing unrelated content.

## Required invariants

- Action → visible result → observation → question/continuation. Preserve canonical cause, order and reveal timing; accidents are not player punishment.
- One object across idle/drag/placed states. Real pictured targets define hit regions; use image coordinates and check both desktop sizes.
- Decode backgrounds **and sprites** before enabling controls; failed loading blocks the scene with Retry. Cancel stale callbacks, blur/hidden gestures and abandoned input. Reduced motion changes presentation, not outcomes.
- Hide answer-bearing captions **and expanded reading** during Quiz; offer explicit return to evidence instead. Wrong answers never complete a checkpoint.
- Language, refresh, replay and rendering must not mutate committed facts. Keep stable scene/option IDs, validate saved data, preserve learned clues and save only committed outcomes.
- Characters move only through fixed story actions. Use clean backgrounds plus independent layers for continuous motion; never slide a rectangular full illustration to imitate walking.
- Preserve private inputs and the user's publication scope. Publishing this toolkit does not publish a supplied book or confer rights in third-party characters/art. Existing explicit publication authorization is sufficient; do not ask for it again.

## Handoff

Run `python3 scripts/validate_book.py PROJECT/book` and `python3 scripts/validate_production.py PROJECT`. A successful structural check does not confirm source truth, artistic quality or browser behavior. Follow the QA matrix, package only intended runtime assets and editable records, and report complete/partial coverage, exact tests, dependencies and remaining human review. The public toolkit's tests are regression evidence; do not claim independent full-DM1 reproduction without actually making and reviewing that book.
