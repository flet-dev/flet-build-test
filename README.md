# flet-build-test

This repository hosts a minimal Flet app used to validate the [`flet build`](https://docs.flet.dev/cli/flet-build/) across platforms.

## GitHub Action: Flet Build

The workflow lives at `.github/workflows/build.yml` and runs on:
- manual dispatch
- a daily cron schedule (12:00 noon UTC)
- pushes to `main` or `dev` (ignores README/license-only changes)
- pull requests (ignores README/license-only changes)

### What it does

Each job:
- installs `uv` and creates a Python venv
- installs `flet[all]` dev dependency - this will correspond to the latest released Flet version (pre-releases included)
- reads the Flet and Flutter versions from `flet.version` module
- pins all `flet*` dependencies in `pyproject.toml` to that Flet version via
  `.github/workflows/scripts/pin_flet_deps.py`, to ensure `flet build` uses the same version to build its app
- installs Flutter SDK corresponding to the read version 
- runs `flet build` for the target platform
