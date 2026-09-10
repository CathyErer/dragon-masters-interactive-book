# Local candidate 0.2.0 verification

2026-09-09. This is a local review candidate, not a published release.

- Skill structure validator: passed.
- Standalone starter copied to a new directory containing spaces: passed; six referenced art/audio resources validated.
- Chrome browser regression at 1280×800 and 1440×900 with reduced motion: 28 assertions passed, zero page errors on the final run.
- Covered observe/drag/hold, repeated blur cancellation, release-to-commit, result before Quiz, hidden answer caption, saved progress/language, sparse fast input on the separate fixed-track component and cleanup.
- Inspected the original SVG lamp-result screenshot. These illustrations demonstrate the mechanism, not a finished 2.5D book style.
- An intermittent negative audio-fade fraction was found in an earlier run and fixed by clamping the interpolation fraction to [0,1]. The final run passed.
- Public hygiene scan found no flagged private paths, emails, key-like strings or unreviewed file types. This heuristic is not a rights review or security guarantee.

Not established: independent full-book reproduction from a new user's source, trace-specific regression, classroom acceptance, subjective music quality, publication rights, license selection or remote release.

Run `python3 scripts/audit_public.py` from the repository root. Browser tests are in `tests/browser.cjs`; optional `OUTPUT_REPORT` and `SCREENSHOT_DIR` save local evidence without embedding machine-specific paths into this toolkit.
