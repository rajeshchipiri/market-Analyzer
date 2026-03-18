# 📖 API Documentation: Trade Opportunities API

This document provides a comprehensive reference for the **Mini Intelligent Market Analysis System** API.

## 🚀 Base URL
The API is versioned and all endpoints (except root) are prefixed with `/api/v1`.
- **Development**: `http://127.0.0.1:8000/api/v1`
- **Interactive Search UI**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔎 Intelligent Search Engine
The system integrates a real-time market data collector that fetches the latest news, investment trends, and sector-specific data from across the web using **DuckDuckGo Search**. This ensures that the AI analysis is always based on the most current information available.

---

## 🔐 Authentication
The API uses **JWT (JSON Web Token)** Bearer authentication for protected endpoints.

### 1. Obtain Access Token
**Endpoint**: `POST /auth/token`  
**Description**: Exchanges credentials for a temporary access token.  
**Content-Type**: `application/x-www-form-urlencoded`

**Request Body (Form Data)**:
| Field | Type | Description |
| :--- | :--- | :--- |
| `username` | String | User's username (Guest mode: any username works) |
| `password` | String | User's password (Guest mode: any password works) |

**Response (200 OK)**:
```json
{
  "access_token": "your_jwt_here...",
  "token_type": "bearer"
}
```

### 2. Use the Token
Include the token in the `Authorization` header for all protected requests:
```text
Authorization: Bearer <your_access_token>
```

---

## 📊 Endpoints

### 🔍 Analyze Sector
**Endpoint**: `GET /analyze/{sector}`  
**Description**: Collects real-time data and generates a high-level strategic market report using Gemini AI.  
**Auth Required**: Yes (Bearer Token)  
**Rate Limit**: Applied per user.

**Path Parameters**:
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `sector` | String | Name of the sector (e.g., `IT`, `Fintech`, `Agriculture`). Min 2 chars. |

**Success Response (200 OK)**:
- **Content-Type**: `text/markdown`
- **Body**: The raw Markdown report content.
- **Header**: `Content-Disposition: attachment; filename=<sector>_report.md`

**Error Responses**:
| Code | Meaning | Reason |
| :--- | :--- | :--- |
| `400` | Bad Request | Invalid sector name (e.g., empty or too short). |
| `401` | Unauthorized | Missing or invalid Bearer token. |
| `429` | Too Many Requests | Rate limit exceeded for this endpoint. |
| `502` | Bad Gateway | Upstream AI service (Gemini) or Search failed. |

---

## 🛠️ Usage Examples (cURL)

### Step 1: Login
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/auth/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=guest&password=pass'
```

### Step 2: Analyze Sector
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/analyze/fintech' \
  -H 'Authorization: Bearer <YOUR_TOKEN_HERE>' \
  -o fintech_report.md
```

---

## 🏗️ Data Models

### 📦 Token
| Field | Type | Description |
| :--- | :--- | :--- |
| `access_token` | String | The JWT access token string. |
| `token_type` | String | Typically "bearer". |

### 📦 ErrorResponse
| Field | Type | Description |
| :--- | :--- | :--- |
| `detail` | String | Explanation of the error encountered. |

---
*Created with ❤️ by Antigravity for the Mini Intelligent Market Analysis System.*
