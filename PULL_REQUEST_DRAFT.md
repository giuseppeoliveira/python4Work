# Draft PR: consolidate project layout, rename NoLog → NoLogout, enforce corporate theme

Branch: feature/restructure_blue_ui
Target: main

Summary
-------
This PR centralizes the repository under `python4Work/`, renames the `NoLog` package to `NoLogout` (and updated exports/imports), enforces the corporate blue theme in the professional UI, removes the theme selector, and adds a modal progress popup for long-running operations.

It also archives legacy files that were living at the workspace root into:
`python4Work/archive_removed_by_refactor/external_root_20251112/`.

What I changed (high level)
- Moved and archived legacy root files into the project archive folder
- Renamed package `src/nolog` → `src/nologout` and updated class names and exports
- Fixed syntax/indentation issues introduced by automated renames
- Enforced 'corporate' theme in `interfaces/interface_profissional.py`
- Removed theme selector UI and added modal progress popup
- Added a lightweight smoke test script (`scripts/run_smoke.py`) and CI workflow
- Added documentation note about consolidation in `README.md`

Smoke tests
-----------
I ran the non-GUI smoke checks locally; results: SMOKE TESTS PASSED.

Manual steps for reviewers
-------------------------
1. Run the app locally: `python main.py` (requires a display). Open the 'Python4Work Professional' UI and click the "🛡️ NoLogout - Manter Sessão" card. Verify NoLogout window opens and start/stop works.
2. Validate that old top-level files are no longer in the repository root. The archived copies are in `archive_removed_by_refactor/external_root_20251112/`.

Notes / Follow-ups
------------------
- If you want the archive removed from the main tree, I recommend moving the archive into a separate backup branch and removing it from the working tree (I created `backup/archive-20251112` locally). Alternatively, we can zip the archive and remove the unpacked folder.
- CI runs the smoke script; GUI tests remain manual due to GUI requirement.

Checklist for PR
----------------
- [ ] Review renamed package imports across the codebase
- [ ] Run manual GUI smoke test (open `main.py` and test NoLogout start/stop)
- [ ] Optional: approve archive removal or archiving policy

If you'd like, create this PR in GitHub and mark as draft. If you prefer, I can try to create the draft PR via the GitHub CLI (requires `gh` installed), or you can open it quickly via:

https://github.com/giuseppeoliveira/python4Work/compare/main...feature/restructure_blue_ui?expand=1
