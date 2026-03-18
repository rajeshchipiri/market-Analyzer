import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.config import settings
from utils.rate_limit import setup_rate_limiting
from routes.api import router as api_router
from utils.logger import setup_logger

logger = setup_logger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="""
# 📊 Trade Opportunities API

A production-level FastAPI service for real-time market intelligence and AI-powered strategic analysis.

### 🎯 Key Features
- **Real-time Data**: Integrated DuckDuckGo search for the latest Indian market news.
- **AI Synthesis**: Specialized Gemini-1.5-Flash analysis for actionable insights.
- **Production Ready**: JWT Auth, Rate Limiting, In-Memory Caching, and Middleware Logging.
""",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        contact={"name": "Backend Engineering Team"},
    )

    # Logging Middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        logger.info(f"Request: {request.method} {request.url.path} - Status: {response.status_code} - Completed in {formatted_process_time}ms")
        return response

    # Health Check Endpoint
    @app.get("/health", tags=["system"], summary="Service health check")
    async def health_check():
        """
        Confirms the API is running and healthy.
        Used by deployment probes and monitoring systems.
        """
        return {"status": "healthy", "service": settings.PROJECT_NAME}

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configure Rate Limiting
    setup_rate_limiting(app)

    # Include Routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/", tags=["health"], response_class=HTMLResponse)
    async def root():
        html_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Mini Intelligent Market Analysis System 📈</title>
                <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f4f7f6;
                        color: #333;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        padding: 40px 20px;
                        margin: 0;
                    }
                    .container {
                        text-align: center;
                        background: #fff;
                        padding: 40px;
                        border-radius: 12px;
                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                        max-width: 900px;
                        width: 100%;
                    }
                    h1 { color: #2c3e50; margin-bottom: 5px; }
                    .tagline { color: #7f8c8d; font-size: 1.1em; margin-bottom: 30px; }
                    
                    /* Search Section */
                    .search-section {
                        background: #f8f9fa;
                        padding: 30px;
                        border-radius: 10px;
                        margin-bottom: 30px;
                        border: 1px solid #e9ecef;
                    }
                    .search-box {
                        display: flex;
                        gap: 10px;
                        margin-bottom: 15px;
                    }
                    input[type="text"] {
                        flex: 1;
                        padding: 12px 20px;
                        border: 2px solid #ddd;
                        border-radius: 6px;
                        font-size: 1em;
                        outline: none;
                        transition: border-color 0.3s;
                    }
                    input[type="text"]:focus { border-color: #007bff; }
                    .search-btn {
                        background-color: #27ae60;
                        color: white;
                        border: none;
                        padding: 12px 24px;
                        border-radius: 6px;
                        font-weight: bold;
                        cursor: pointer;
                        transition: background 0.3s;
                    }
                    .search-btn:hover { background-color: #219150; }
                    
                    .auth-tip { font-size: 0.9em; color: #666; margin-top: 10px; }

                    /* Results Section */
                    #resultsArea {
                        display: none;
                        text-align: left;
                        background: #fff;
                        padding: 30px;
                        border-radius: 10px;
                        border: 1px solid #eee;
                        margin-top: 30px;
                        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
                    }
                    #resultsContent { line-height: 1.6; }
                    #resultsContent h1, #resultsContent h2 { color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }
                    #resultsContent code { background: #f4f4f4; padding: 2px 5px; border-radius: 4px; }

                    .grid {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 20px;
                        text-align: left;
                        margin-bottom: 30px;
                    }
                    .card {
                        background: #fcfcfc;
                        padding: 20px;
                        border-radius: 8px;
                        border-left: 4px solid #007bff;
                    }
                    .card h3 { margin-top: 0; color: #34495e; font-size: 1.1em; }
                    .card p { margin-bottom: 5px; color: #555; font-size: 0.95em; }
                    
                    .button-group { margin-top: 20px; display: flex; gap: 10px; justify-content: center; }
                    a.button {
                        display: inline-block;
                        background-color: #007bff;
                        color: #fff;
                        padding: 12px 24px;
                        text-decoration: none;
                        border-radius: 6px;
                        font-weight: bold;
                        transition: background-color 0.3s;
                    }
                    a.button:hover { background-color: #0056b3; }
                    a.button.secondary { background-color: #6c757d; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Trade Opportunities API 📊</h1>
                    <p class="tagline">Real-time market intelligence & AI-powered strategic analysis.</p>
                    
                    <div class="search-section">
                        <h3>Search for Sector Analysis</h3>
                        <div class="search-box">
                            <input type="text" id="sectorInput" placeholder="Enter sector (IT, technology, agriculture)...">
                            <button class="search-btn" id="genBtn" onclick="startAnalysis()">Generate Report</button>
                        </div>
                        <p class="auth-tip" id="statusMsg">Note: Authentication is required. Use the button below to get a demo token first.</p>
                        <button id="tokenBtn" onclick="getDemoToken()" style="background:none; border:none; color:#007bff; cursor:pointer; text-decoration:underline;">Click here to set Demo Token</button>
                    </div>

                    <div id="resultsArea">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h2 style="margin:0;">Analysis Result</h2>
                            <button onclick="downloadMarkdown()" style="background:#007bff; color:white; border:none; padding:8px 16px; border-radius:4px; cursor:pointer;">Download .md File</button>
                        </div>
                        <div id="resultsContent"></div>
                    </div>

                    <div class="grid">
                        <div class="card">
                            <h3>🔍 Search</h3>
                            <p>Fetches latest trends, news, and investments from across the web.</p>
                        </div>
                        <div class="card" style="border-left-color: #27ae60;">
                            <h3>🤖 AI Analysis</h3>
                            <p>Uses Gemini AI to find patterns, opportunities, and risks specialized for the Indian market.</p>
                        </div>
                    </div>

                    <div class="button-group">
                        <a href="/docs" class="button secondary">View API Docs (Swagger)</a>
                    </div>
                </div>

                <script>
                    let accessToken = localStorage.getItem('demo_token');
                    let lastReportMarkdown = "";
                    let lastSector = "";

                    if (accessToken) {
                        document.getElementById('statusMsg').innerText = "Demo token is set! You can search now.";
                        document.getElementById('tokenBtn').style.display = "none";
                    }

                    async function getDemoToken() {
                        try {
                            const formData = new URLSearchParams();
                            formData.append('username', 'guest_user');
                            formData.append('password', 'password123');
                            
                            const response = await fetch('/api/v1/auth/token', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                                body: formData
                            });
                            const data = await response.json();
                            if (data.access_token) {
                                localStorage.setItem('demo_token', data.access_token);
                                alert("Demo token successfully generated!");
                                location.reload();
                            }
                        } catch (e) {
                            alert("Failed to get token: " + e);
                        }
                    }

                    async function startAnalysis() {
                        const sectorInput = document.getElementById('sectorInput');
                        const sector = sectorInput.value.trim();
                        let token = localStorage.getItem('demo_token');
                        
                        if (!sector) { alert("Please enter a sector name."); return; }

                        const status = document.getElementById('statusMsg');
                        const btn = document.getElementById('genBtn');
                        const resultsArea = document.getElementById('resultsArea');
                        const resultsContent = document.getElementById('resultsContent');

                        console.log("Starting analysis for:", sector);

                        // Auto-fetch token if missing
                        if (!token) {
                            console.log("No token found. Attempting auto-auth...");
                            status.innerText = "Initializing secure session... (Auto-authenticating)";
                            try {
                                const formData = new URLSearchParams();
                                formData.append('username', 'guest_investor');
                                formData.append('password', 'secure_pass_123');
                                const authRes = await fetch('/api/v1/auth/token', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                                    body: formData
                                });
                                
                                if (!authRes.ok) throw new Error("Auth endpoint returned " + authRes.status);
                                
                                const authData = await authRes.json();
                                if (authData.access_token) {
                                    token = authData.access_token;
                                    localStorage.setItem('demo_token', token);
                                    console.log("Auto-auth successful.");
                                } else {
                                    throw new Error("Token missing in response");
                                }
                            } catch (e) {
                                console.error("Auto-auth failed:", e);
                                status.innerText = "Error: Session initialization failed. Please refresh the page.";
                                return;
                            }
                        }

                        status.innerText = "Analyzing " + sector + "... please wait (fetching data and AI processing).";
                        btn.disabled = true;
                        btn.innerText = "Processing...";
                        resultsArea.style.display = "none";
                        
                        try {
                            console.log("Fetching analysis from API...");
                            const response = await fetch('/api/v1/analyze/' + encodeURIComponent(sector), {
                                headers: { 'Authorization': 'Bearer ' + token }
                            });
                            
                            if (response.status === 200) {
                                const text = await response.text();
                                console.log("Analysis received successfully.");
                                lastReportMarkdown = text;
                                lastSector = sector;
                                resultsContent.innerHTML = marked.parse(text);
                                resultsArea.style.display = "block";
                                status.innerText = "Analysis complete!";
                                resultsArea.scrollIntoView({ behavior: 'smooth' });
                            } else if (response.status === 401) {
                                console.warn("Token expired or invalid (401). Clearing and retrying once...");
                                localStorage.removeItem('demo_token');
                                startAnalysis(); // Recursive retry once
                                return;
                            } else {
                                throw new Error("API returned " + response.status);
                            }
                        } catch (err) {
                            console.error("API error:", err);
                            status.innerText = "Error: " + err.message;
                        } finally {
                            btn.disabled = false;
                            btn.innerText = "Generate Report";
                        }
                    }

                    function downloadMarkdown() {
                        if (!lastReportMarkdown) return;
                        const blob = new Blob([lastReportMarkdown], { type: 'text/markdown' });
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = lastSector + "_report.md";
                        document.body.appendChild(a);
                        a.click();
                        a.remove();
                    }
                </script>
            </body>
        </html>
        """
        return html_content

    @app.get("/analyze/{sector}", tags=["analysis"], include_in_schema=False)
    async def analyze_redirect(sector: str):
        """Redirect for strictly following the prompt's specified endpoint path."""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=f"{settings.API_V1_STR}/analyze/{sector}")

    # Global Exception Handler Example
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."}
        )

    logger.info("FastAPI application created successfully.")
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    # Make sure this points to the right module location based on working directory
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
