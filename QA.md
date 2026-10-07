# 0.3.0 verification — 2026-10-07

- Skill structure validator: PASS.
- Project/coverage contracts: **14/14** PASS (`python3 tests/contracts.py`).
- Original demo/component regression: **28/28** PASS (`node tests/browser.cjs`).
- Production-engine fixture: **41/41** PASS (`node tests/production-browser.cjs`).
- Browser runs: real local Chrome at 1280×800 normal and 1440×900 reduced motion; zero script errors on final runs. JavaScript and Python syntax checks passed.
- Checks include source-driven cover/ending, intermediate scenes without Quiz, fixed-track endpoint commitment/cancellation, retained completed sprite, progress-preserving replay, answer isolation including expanded reading/Journal, wrong answers, optional retell/reload/closing, missing-sprite retry, and identical prop dimensions before/after placement.
- Screenshots of the original demo and production-engine fixture were inspected. They are functional SVG examples, not a new DM1 illustration set. A new geometry regression exposed intrinsic image height overriding the requested prop ratio; explicit image-frame dimensions fixed it and the final test passes.
- `tests/results-0.3.0.json` contains individual assertions, current runtime hashes and exact scope. Test fixture metadata is synthetic and is never evidence of source-book acceptance.

## Independent original-source trial

An isolated agent received only the public Skill and an original two-chapter story. It produced 8 scenes, 2 chapter quizzes, 1 optional retell, new SVG art and the production records. Runtime dependency validation (15 assets), JavaScript syntax and extraction to a fresh directory containing spaces passed.

The production gate correctly remains incomplete: `in-review` plus 8 pending browser, visual and listening checks, with no chapter mapping, continuity, provenance or hash errors. The trial browser refused local-file navigation on policy grounds; no alternative route was attempted. This is a limited independent workflow trial, not browser acceptance or a full DM1 reproduction.

The trial found four gaps now repaired in the public source: original-profile documentation, hard-coded demo cover strings/background, a mechanical “Turn” keyboard label for non-turning actions, and configurable long-prop geometry.

## Reproduce and interpret

Python scripts use the standard library. Browser tests need Playwright; `PLAYWRIGHT_MODULE` and `CHROME_PATH` can point at an installed runtime. `OUTPUT_REPORT` and `SCREENSHOT_DIR` save results outside the repository. Public file scanning: `python3 scripts/audit_public.py`. Build and member-hash checks: `python3 scripts/package_candidate.py --destination NEW_DIRECTORY`.

Not established: a new user's complete 16-chapter DM1 adaptation, trace-specific browser regression, subjective music quality, classroom results, or teacher acceptance of a newly generated book. Publishing a tested toolkit does not establish those claims.
