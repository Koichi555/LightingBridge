# API Contract — LightingBridge v1.0.1

## Overview

This document defines the HTTP API contract between the LightingBridge backend and the local web UI. All interfaces must conform to this contract. Any breaking change requires a version increment.

**Base URL:** `http://127.0.0.1:5000`  
**Protocol:** HTTP/1.1 (local only, no TLS required for offline deployment)  
**Content-Type:** `application/json`

---

## 1. Response Wrapper

All API responses **must** use the following unified wrapper:

```json
{
  "code": 200,
  "data": {},
  "msg": "success"
}
```

| Field | Type | Description |
|---|---|---|
| `code` | integer | HTTP-aligned status code (200, 400, 404, 500) |
| `data` | any | Response payload. `null` on error. |
| `msg` | string | Human-readable result description |

The wrapper format must remain **stable across all patch and minor versions**. Breaking wrapper changes require a major version bump.

---

## 2. Endpoints

### 2.1 Service Health Check

**GET** `/`

Purpose: Verify the backend service is running.

**Response:**
```json
{
  "code": 200,
  "data": { "service": "LightingBridge Backend" },
  "msg": "success"
}
```

---

### 2.2 Get Load Configuration

**GET** `/api/config/loads`

Purpose: Return all configured loads for UI rendering. Called once on UI startup.

**Response:**
```json
{
  "code": 200,
  "data": [
    {
      "tagKey": "Panel01::Light01",
      "name": "Barn A Light 01",
      "group": "Barn A",
      "writable": true
    },
    {
      "tagKey": "Panel01::Light02",
      "name": "Barn A Light 02",
      "group": "Barn A",
      "writable": false
    }
  ],
  "msg": "success"
}
```

**Load Object Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `tagKey` | string | Yes | Globally unique tag identifier. Format: `Panel::LoadName` |
| `name` | string | Yes | Display name shown in UI |
| `group` | string | Yes | Group label for UI grouping |
| `writable` | boolean | Yes | Whether write commands are allowed for this load |

---

### 2.3 Bulk Status Fetch

**POST** `/api/status/bulk`

Purpose: Return current status for a list of tag keys. Called periodically by the UI polling loop.

**Request:**
```json
{
  "tagKeys": ["Panel01::Light01", "Panel01::Light02"]
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `tagKeys` | array of strings | Yes | List of tagKeys to query. Must be a JSON array. |

**Response:**
```json
{
  "code": 200,
  "data": {
    "Panel01::Light01": {
      "value": true,
      "quality": "good",
      "ts": "2026-03-14T10:00:00+08:00"
    },
    "Panel01::Light02": {
      "value": false,
      "quality": "good",
      "ts": "2026-03-14T10:00:00+08:00"
    }
  },
  "msg": "success"
}
```

**Status Object Fields:**

| Field | Type | Description |
|---|---|---|
| `value` | boolean | Current on/off state |
| `quality` | string | Data quality: `good`, `bad`, `uncertain` |
| `ts` | string | ISO 8601 timestamp with timezone |

**Error — Invalid Request:**
```json
{
  "code": 400,
  "data": null,
  "msg": "tagKeys must be a list"
}
```

---

### 2.4 Write Command

**POST** `/api/command/write`

Purpose: Submit a write command from the UI to the backend command queue.

**Request:**
```json
{
  "tagKey": "Panel01::Light01",
  "desiredOn": true,
  "source": "UI"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `tagKey` | string | Yes | Target load tag key |
| `desiredOn` | boolean | Yes | Target state: `true` = ON, `false` = OFF |
| `source` | string | No | Origin of command. Default: `"UI"` |

**Response:**
```json
{
  "code": 200,
  "data": {
    "accepted": true,
    "queueId": "CMD-2026-03-14T10:00:00+08:00",
    "tagKey": "Panel01::Light01",
    "desiredOn": true,
    "source": "UI"
  },
  "msg": "success"
}
```

**Error — Missing tagKey:**
```json
{
  "code": 400,
  "data": null,
  "msg": "tagKey is required"
}
```

**Error — Invalid desiredOn type:**
```json
{
  "code": 400,
  "data": null,
  "msg": "desiredOn must be boolean"
}
```

---

### 2.5 Recent Logs

**GET** `/api/logs/recent`

Purpose: Return recent operation and system logs for UI display and troubleshooting.

**Response:**
```json
{
  "code": 200,
  "data": [
    {
      "ts": "2026-03-14T10:00:05+08:00",
      "level": "INFO",
      "message": "Write accepted: Panel01::Light01 -> ON"
    },
    {
      "ts": "2026-03-14T09:59:50+08:00",
      "level": "WARNING",
      "message": "Modbus read timeout on device 192.168.1.10"
    }
  ],
  "msg": "success"
}
```

**Log Entry Fields:**

| Field | Type | Description |
|---|---|---|
| `ts` | string | ISO 8601 timestamp with timezone |
| `level` | string | Log level: `INFO`, `WARNING`, `ERROR` |
| `message` | string | Human-readable log message |

---

## 3. Error Handling

All error responses follow the same wrapper:

```json
{
  "code": 500,
  "data": null,
  "msg": "modbus write failed"
}
```

| Code | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad request (validation failed) |
| 404 | Resource not found |
| 500 | Internal server error |

---

## 4. Contract Rules

- `tagKey` must be **globally unique** across all configured loads
- `desiredOn` accepts **boolean only** (`true`/`false`). String values like `"yes"` or `"1"` are rejected with 400
- All timestamps must be **ISO 8601** with timezone offset (e.g., `+08:00`)
- The response wrapper `{code, data, msg}` must remain stable across patch and minor versions
- Response wrapper changes require a major version bump
- The `quality` field in status response uses: `good`, `bad`, `uncertain`
- `writable: false` loads will not be executed even if a write command is submitted

---

## 5. Versioning

This contract applies to: **Backend v1.0.1 + UI v1.0.2**

Breaking changes to this contract require:
1. Major version increment (e.g., `v2.0.0`)
2. Update of this document
3. Update of `CHANGELOG.md`
4. Communication to all integrators

---

## 6. Related Documents

- `docs/testing/TEST_PLAN.md` — Test cases that validate this contract
- `docs/architecture/BACKEND_ARCHITECTURE.md` — Backend layer design
- `docs/deployment/DEPLOYMENT_GUIDE.md` — How to run the service
- `backend/app/api/` — Route implementations
