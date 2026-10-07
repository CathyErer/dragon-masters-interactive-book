# Dragon Masters Interactive Book 0.3.0

CathyErer · MIT · 2026-10-07. This update completes the public production workflow and repairs the starter behavior exposed by independent use.

## Changes

- Full Book 1 route: 16 chapter checkpoints, source/event/scene coverage, character and scene planning, image/music prompts, asset provenance and actual QA records.
- Separate production workspace and explicit original demo; independent save IDs. Original-source profile documented.
- Integrated fixed-track sprites, retained endpoints and non-destructive replay; action-aware keyboard labels and configurable prop geometry.
- Multiple scenes per chapter with optional Quiz; source-driven cover/background/ending, evidence Journal and optional keyword retells.
- Question mode hides expanded reading, captions and Journal; missing background/sprite blocks controls and offers Retry.
- Complete-production validator rejects missing chapters/events, discontinuities, missing provenance and stale QA hashes. No placeholder may be called a complete book.

## Packages

Run `python3 scripts/package_candidate.py --destination NEW_DIRECTORY` from the repository root. It creates:

- `Dragon Masters Interactive Book.zip`: full public repository content, excluding Git internals.
- `dragon-masters-interactive-book.skill`: installable Skill-folder ZIP for clients that support it.
- `Dragon Masters Interactive Book.manifest.json`: file/member hashes and installation-package SHA256.

Both archives are reproducible from the same source. The source Skill is `skills/dragon-masters-interactive-book/`; the repository wrapper is not the install root. Root and Skill directories retain the existing MIT license. Original demo SVG/WAV assets are MIT; user books and third-party character/reference assets are not included or licensed by this package.

## Verification and limits

83 final contract/browser assertions passed (14 + 28 + 41), plus structure/syntax checks. Detailed evidence and the limited independent original-source trial are in QA.md. Complete DM1 independent reproduction and classroom acceptance remain unverified.

Repository: https://github.com/CathyErer/dragon-masters-interactive-book
