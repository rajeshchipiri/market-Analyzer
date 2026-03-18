import json
import time
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
from fastapi import HTTPException, status

from utils.config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SimpleCache:
    """A basic in-memory cache with TTL."""
    def __init__(self, ttl_seconds: int = 3600):
        self._cache = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[str]:
        if key in self._cache:
            entry = self._cache[key]
            if time.time() - entry['timestamp'] < self._ttl:
                logger.info(f"Cache hit for key: {key}")
                return entry['data']
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: str):
        self._cache[key] = {
            'data': value,
            'timestamp': time.time()
        }

class DataCollector:
    """Service for collecting market data using DuckDuckGo Search."""
    
    def search_market_data(self, sector: str) -> List[Dict[str, Any]]:
        # Query format as per requirement: "{sector} sector India news 2026"
        query = f"{sector} sector India news 2026"
        results = []
        logger.info(f"Searching market data with query: {query}")
        
        try:
            with DDGS() as ddgs:
                # Extract title + body, limit to 5 results
                raw_results = list(ddgs.text(query, max_results=5))
                for r in raw_results:
                    results.append({
                        "title": r.get("title", ""),
                        "body": r.get("body", "")
                    })
                    
            logger.info(f"Successfully retrieved {len(results)} search results for {sector}")
            return results
        except Exception as e:
            logger.error(f"Error fetching data from DuckDuckGo: {e}")
            if not results:
                 raise HTTPException(
                     status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                     detail=f"Temporary search engine error for '{sector}'. Please try again."
                 )
            return results

class AIAnalyzer:
    """Service for analyzing data and generating reports using Google Gemini."""
    
    def __init__(self):
        import google.generativeai as genai
        self.genai = genai
        self.model_name = "gemini-1.5-flash"
        self.is_configured = False
        self._cache = SimpleCache(ttl_seconds=settings.CACHE_TTL if hasattr(settings, 'CACHE_TTL') else 3600)
        
        if settings.GEMINI_API_KEY:
            try:
                self.genai.configure(api_key=settings.GEMINI_API_KEY)
                self.is_configured = True
                logger.info("GenAI (Gemini 1.5 Flash) configured successfully.")
            except Exception as e:
                logger.warning(f"Failed to configure GenAI: {e}")
        else:
             logger.warning("GEMINI_API_KEY missing. Running in mock mode.")
             
    def generate_report(self, sector: str, search_data: List[Dict[str, Any]]) -> str:
        # Check cache first
        cached_report = self._cache.get(sector)
        if cached_report:
            return cached_report

        if not self.is_configured:
            logger.info("Using mock AI generation (API key missing)")
            report = self._generate_mock_report(sector, search_data)
            self._cache.set(sector, report)
            return report
            
        logger.info(f"Generating AI report for sector: {sector}")
        try:
            model = self.genai.GenerativeModel(self.model_name)
            
            # Combine logic as requested into single text block
            data_block = "\n---\n".join([f"TITLE: {item['title']}\nBODY: {item['body']}" for item in search_data])
            
            # Exact Prompt Template from requirement
            prompt = f"""
You are a senior market intelligence analyst specializing in Indian markets.

Analyze the {sector} sector using the data below.

DATA:
{data_block}

INSTRUCTIONS:
- Use only the given data
- Do not hallucinate
- Avoid generic statements
- Focus on India
- Be concise but insightful

OUTPUT FORMAT (STRICT MARKDOWN):

# 📊 {sector} Sector Analysis (India)

## 🧾 Overview
(3-4 lines)

## 📈 Key Trends
- 4-6 trends

## 🚀 Opportunities
- 4-6 opportunities

## ⚠️ Risks & Challenges
- 4-5 risks

## 💡 Strategic Insights
- 2-3 expert insights

## 🧠 Conclusion
- Future outlook

RULES:
- No extra text outside markdown
- No placeholders
"""
            
            response = model.generate_content(prompt)
            report = response.text.strip()
            
            # Clean up potential markdown wrappers
            if report.startswith("```markdown"): report = report[11:]
            if report.startswith("```"): report = report[3:]
            if report.endswith("```"): report = report[:-3]
            
            final_report = report.strip()
            self._cache.set(sector, final_report)
            return final_report
            
        except Exception as e:
            logger.error(f"Gemini API failure: {e}")
            # Fallback response as requested
            return self._generate_mock_report(sector, search_data)

    def _generate_mock_report(self, sector: str, search_data: List[Dict[str, Any]]) -> str:
        """Fallback mock report when AI service is unavailable."""
        snippets = "\n".join([f"- {item.get('title')}: {item.get('body')[:100]}..." for item in search_data[:3]])
        return f"""# 📊 {sector.capitalize()} Sector Analysis (India)

## 🧾 Overview
Analysis of the {sector} sector based on recent market shifts in 2026. This sector shows significant realignment towards domestic manufacturing and digital-first logistics.

## 📈 Key Trends
- Rapid adoption of AI-integrated supply chain solutions
- Government focus on PLI schemes for local manufacturing
- Shift towards green energy and sustainable trade practices
- Increasing venture capital flow into early-stage fintech

## 🚀 Opportunities
- Expansion into Tier 2 and Tier 3 cities via regional distribution hubs
- Localization of component sourcing to mitigate global supply risks
- Integration of blockchain for transparent contract management
- Emerging B2B marketplaces for specialized industrial equipment

## ⚠️ Risks & Challenges
- Regulatory changes regarding cross-border data privacy
- Volatility in global raw material prices
- Talent shortage in specialized technical roles
- Infrastructure bottlenecks in emerging industrial zones

## 💡 Strategic Insights
- Focus on building platform-independent digital infrastructure.
- Prioritize operational efficiency through automated warehouse management.

## 🧠 Conclusion
The {sector} sector is poised for steady growth through 2026, driven by strong internal demand and supportive policy frameworks.
"""

# Helper functions for Dependency Injection
def get_data_collector():
    return DataCollector()

def get_ai_analyzer():
    return AIAnalyzer()
