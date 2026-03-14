# GitHub Release Strategy

## Overview

This document defines what belongs in the Git repository versus what belongs in GitHub Releases, and how versioned deliverables are named and published.

---

## What Goes Into the Git Repository

The repository stores all maintainable, traceable, and collaborative assets:

- Backend source code (`backend/`)
- Frontend UI source code (`ui/`)
- Excel configuration templates (`config_templates/`)
- API contract documentation (`docs/api/`)
- Architecture documentation (`docs/architecture/`)
- Deployment guides (`docs/deployment/`)
- Test plans and test cases (`docs/testing/`)
- Project management documents (`docs/project_management/`)
- Build and packaging scripts (`scripts/`)
- Release notes and manifest records (`release/`)
- CI workflow definitions (`.github/workflows/`)

---

## What Should NOT Go Into the Git Repository

The following must be excluded and are covered by `.gitignore`:

- `_internal/` — PyInstaller runtime bundle
- Large `.exe` binaries
- Python embed runtime
- Runtime logs (`logs/`, `*.log`)
- Output ZIP deployment packages (`*.zip`)
- Site-specific production Excel files (`config/*.xlsx`)
- Secrets, credentials, `.env` files
- Customer-specific runtime databases
- Large test recordings or raw video evidence

---

## What Goes Into GitHub Releases

Each tagged version publishes the following as release attachments:

| File | Description |
|---|---|
| `LightingBridge_vX.Y.Z_win-x64.zip` | Full deployment package |
| `LightingBridge_vX.Y.Z_manifest.json` | Artifact manifest |
| `LightingBridge_vX.Y.Z_SHA256SUMS.txt` | Checksum file |
| `LightingBridge_vX.Y.Z_deployment_guide.pdf` | Deployment guide |
| `LightingBridge_vX.Y.Z_release_notes.pdf` | Release notes |

---

## Version Tagging

This project follows [Semantic Versioning](https://semver.org/):

| Tag | When to Use |
|---|---|
| `vX.Y.Z` PATCH | Bug fix or packaging correction |
| `vX.Y.Z` MINOR | New backward-compatible feature |
| `vX.Y.Z` MAJOR | Breaking API or config format change |

Current target: `v1.0.1`

---

## Release Naming Convention

Example for version `v1.0.1`:

```
LightingBridge_v1.0.1_win-x64.zip
LightingBridge_v1.0.1_manifest.json
LightingBridge_v1.0.1_SHA256SUMS.txt
LightingBridge_v1.0.1_deployment_guide.pdf
LightingBridge_v1.0.1_release_notes.pdf
```

---

## Deployment ZIP Internal Structure

```
LightingBridge_v1.0.1/
├─ LightingBridge.exe
├─ _internal/
├─ config/
│   ├─ devices.xlsx
│   ├─ loads.xlsx
│   ├─ mapping.xlsx
│   └─ feedlink.xlsx
├─ ui/
├─ logs/
├─ run_backend.bat
├─ manifest.json
└─ README_DEPLOY.txt
```

---

## Release Branch and Tag Flow

1. Feature development on `feature/*` branches
2. Merge to `develop` for integration testing
3. Create `release/vX.Y.Z` branch for stabilization
4. Run full test checklist
5. Merge to `main`
6. Create Git tag: `git tag vX.Y.Z`
7. Generate manifest and checksum
8. Build deployment ZIP
9. Publish GitHub Release with all attachments

---

## Principles

- The Git repository is for **maintainability and traceability**
- GitHub Releases are for **deployable deliverables**
- Source, docs, and templates are versioned in Git
- Runtime bundles, ZIPs, and binaries are distributed through Releases only
- Never commit `_internal/`, `.exe`, or deployment ZIPs to Git
