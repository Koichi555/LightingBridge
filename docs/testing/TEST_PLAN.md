# Test Plan — LightingBridge v1.0.1

## 1. Objective

Validate that LightingBridge can be deployed on a Windows machine in an offline environment and provide stable status monitoring and write control for all configured Modbus loads.

---

## 2. Scope

### In Scope
- Backend startup and initialization
- Excel configuration loading (devices, loads, mapping, feedlink)
- Modbus TCP polling and status normalization
- REST API responses (config, status, command, logs)
- Web UI rendering and interaction
- Write command acceptance and queuing
- Error handling and structured error responses
- Offline operation (no internet dependency)
- Packaged deployment on a clean Windows machine

### Out of Scope
- Physical Modbus device field testing (covered separately)
- Load-test / stress-test under high traffic
- Browser compatibility beyond local Chromium
- Multi-user concurrent access

---

## 3. Test Environment

| Item | Specification |
|---|---|
| OS | Windows 10 / Windows 11 |
| Deployment | Packaged exe + `_internal/` |
| Network | Local LAN or loopback only |
| Browser | Local Chromium / Edge |
| Config | Sample Excel templates (sanitized) |
| Modbus device | Simulator or real Modbus TCP device |

---

## 4. Entry Criteria

- [ ] Deployment package built and ready
- [ ] `manifest.json` generated
- [ ] `SHA256SUMS.txt` verified
- [ ] Sample Excel config files available in `config/`
- [ ] Test environment isolated from internet
- [ ] Modbus device or simulator running and reachable

---

## 5. Exit Criteria

- [ ] All TC-001 through TC-010 pass with no blocking issues
- [ ] API responses match contract wrapper format
- [ ] Write commands correctly queued and acknowledged
- [ ] Offline restart succeeds without errors
- [ ] Deployment package is reproducible from scripts

---

## 6. Test Cases

### TC-001 — Backend Startup
- **Action:** Run `run_backend.bat`
- **Expected:** Service starts, no fatal error, port 5000 listening
- **Pass criteria:** Process stays alive, no crash within 30s

### TC-002 — Config Load
- **Action:** Start with valid Excel config files in `config/`
- **Expected:** Devices, loads, mapping loaded without error
- **Pass criteria:** `/api/config/loads` returns configured loads

### TC-003 — UI Access
- **Action:** Open `http://127.0.0.1:5000/` in browser
- **Expected:** UI renders load list and status display
- **Pass criteria:** Page loads fully with no console errors

### TC-004 — Bulk Status API
- **Action:** `POST /api/status/bulk` with valid tagKeys
- **Expected:** Status values returned with quality and timestamp
- **Pass criteria:** Response matches wrapper `{code, data, msg}`

### TC-005 — Write Command API
- **Action:** `POST /api/command/write` with `tagKey`, `desiredOn: true`, `source: UI`
- **Expected:** Command accepted, queueId returned
- **Pass criteria:** `accepted: true`, `queueId` non-empty

### TC-006 — Write Command Validation
- **Action:** `POST /api/command/write` with missing `tagKey`
- **Expected:** 400 error with structured message
- **Pass criteria:** `{code: 400, msg: "tagKey is required"}`

### TC-007 — Write Command Type Check
- **Action:** `POST /api/command/write` with `desiredOn: "yes"` (string instead of bool)
- **Expected:** 400 error
- **Pass criteria:** `{code: 400, msg: "desiredOn must be boolean"}`

### TC-008 — Recent Logs API
- **Action:** `GET /api/logs/recent`
- **Expected:** Recent log entries returned
- **Pass criteria:** Array of log objects with `ts`, `level`, `message`

### TC-009 — Offline Restart
- **Action:** Disconnect machine from internet, restart backend
- **Expected:** System operates normally on local network
- **Pass criteria:** All APIs respond, UI accessible

### TC-010 — Clean Machine Deployment
- **Action:** Deploy package on machine without Python installed
- **Expected:** Backend starts via `run_backend.bat`
- **Pass criteria:** No Python dependency error, UI accessible

---

## 7. Defect Classification

| Severity | Definition |
|---|---|
| P1 Blocking | System cannot start or core API fails |
| P2 Major | Write command or status polling fails |
| P3 Minor | UI cosmetic issue or non-critical log error |
| P4 Trivial | Documentation or label inconsistency |

P1 and P2 defects must be resolved before release gate is passed.

---

## 8. Test Deliverables

- Test case execution log (dated)
- Screenshots for TC-003, TC-005, TC-009
- Error log summary (if any failures)
- Final test conclusion statement
- Signed-off UAT checklist

---

## 9. Responsibilities

| Role | Responsibility |
|---|---|
| Engineer | Execute TC-001 to TC-010, capture evidence |
| Project Manager | Review test results, approve release gate |
| QA Reviewer | Verify defect classification and sign-off |

---

## 10. Related Documents

- `docs/api/API_CONTRACT.md`
- `docs/deployment/DEPLOYMENT_GUIDE.md`
- `docs/testing/TEST_CASES.md`
- `docs/testing/UAT_CHECKLIST.md`
- `docs/project_management/RELEASE_CHECKLIST.md`
