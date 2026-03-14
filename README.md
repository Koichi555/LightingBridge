# LightingBridge
Industrial Modbus Lighting Control Bridge

LightingBridge is an industrial-grade Modbus control gateway that connects field devices to a web-based control interface for local, offline-capable lighting control.

## Features
- Modbus TCP polling engine
- 182+ point control capability
- Web UI terminal
- Offline operation support
- Excel-based configuration
- Command queue + safety lock
- Feedlink rule engine
- Local deployment without Python preinstalled

## Architecture
### Backend
- Python 3.11
- Flask API
- pymodbus
- openpyxl

### Frontend
- Vue 3
- Tailwind CSS
- Lucide Icons

## Repository Structure
```
backend/           Python backend source
ui/                Frontend offline UI and assets
config_templates/  Excel configuration templates
docs/              API, deployment, testing, architecture docs
scripts/           Build and helper scripts
release/           Release notes and packaged build references
```

## Quick Start
1. Copy or edit configuration files in `config_templates/`
2. Build or place the packaged executable in your deployment folder
3. Run: `run_backend.bat`
4. Open: http://127.0.0.1:5000/

## Release
Current target release:
- `v1.0.1` — Final release package with Backend v1.0.1 + UI v1.0.2

See `release/RELEASE_NOTES_v1.0.1.md`.

## Notes
- Do **not** commit large packaged runtime folders like `_internal/` to Git.
- Use GitHub Releases to publish deployment ZIP files.
- Keep source, docs, templates, and test evidence versioned here.

## License
MIT
