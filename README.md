# Trade Opportunities API

A FastAPI-based service that analyzes market opportunities for different sectors. It fetches real-time data, processes it using AI, and returns structured insights. It also includes authentication, rate limiting, and modular architecture for scalability.

## 🧠 Core Concept
**Build an API that takes a sector name → collects market data → analyzes it → returns a smart report.**

### Your System Does:
- 🔎 **Searches data**: News about technology sector, market trends, investments.
- 🤖 **Analyzes it (AI)**: Using Gemini (or mock AI) to find patterns, opportunities, and risks.
- 📊 **Generates report**: Clean structured markdown with Overview, Trends, Opportunities, Risks.

## 🌍 Real-World Meaning
This simulates a real product used by Investors, Businesses, and Analysts to decide where to invest, which sector is growing, and what risks exist.

## Features
- **FastAPI**: Asynchronous web framework for high performance.
- **Data Collection**: Uses DuckDuckGo search to fetch the latest sector news and market data.
- **AI Analysis**: Integrates with Google Gemini API to synthesize data into a structured markdown report.
- **Fallback Mechanism**: Automatically generates dynamic mock reports if the Gemini API key is missing.
- **Security**:
  - JWT Authentication
  - Rate Limiting (SlowAPI)
- **Modular Structure**: Clean separation of concerns (Models, Routes, Services, Utils).

# 📊 Trade Opportunities API

A production-level FastAPI service that provides high-level strategic market insights for the Indian economy.

## 🎯 Project Overview
This system collects real-time market data, processes it using the Google Gemini-1.5-Flash AI model, and generates structured, actionable reports for investors and businesses.

### 🚀 Key Features
- **Intelligent Search**: Real-time data collection using DuckDuckGo.
- **AI Synthesis**: Specialized prompt engineering for "Senior Market Intelligence Analyst" insights.
- **In-Memory Caching**: Fast response times for repeated sector analysis.
- **Production Guardrails**: JWT authentication, rate limiting (5 req/min), and middleware logging.

---

## 🏗️ Project Structure
```text
trade_opportunities_api/
├── main.py           # Application entry point & Middleware
├── routes/           # API Endpoints (Auth, Analysis)
├── services/         # Core Logic (AI, Search, Caching)
├── models/           # Pydantic Schemas
├── utils/            # Security, Config, Logger
└── requirements.txt  # Dependencies
```

---

## 🐳 Deployment (Docker)

To deploy the API in a production environment using Docker:

```bash
# 1. Build the image
docker build -t trade-opportunities-api .

# 2. Run the container
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY="your_api_key" \
  --name trade-api \
  trade-opportunities-api
```

The API will be available at **http://localhost:8000**. Use the `/health` endpoint for monitoring.

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10+
- Google Gemini API Key

### 2. Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set Environment Variables
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Running the Server
```bash
uvicorn main:app --reload
```
```

**Response:**
The API returns a raw Markdown file (`text/markdown`) with a `Content-Disposition` header that prompts your browser to download it as `pharmaceuticals_report.md`.

**Example Content:**
```markdown
# Sector Overview
The Indian pharmaceutical sector is the 3rd largest in the world by volume...

# Latest Trends
...
```
