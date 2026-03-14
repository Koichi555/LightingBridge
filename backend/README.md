# Backend
Python backend source for LightingBridge.

## Responsibilities
- Modbus TCP polling
- Device status normalization
- Write command queue
- Safety lock / debounce control
- Excel configuration loading
- Feedlink rule processing
- REST API service for local UI

## Suggested Structure
```
app/
├─ api/       # Flask routes
├─ services/  # business services
├─ drivers/   # Modbus / field device adapters
├─ models/    # DTO / schema / config model
├─ utils/     # helpers
└─ main.py    # entrypoint
```

## Local Run
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

## Test
```
pytest
```
