from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from models.schemas import Token, ErrorResponse
from utils.security import create_access_token, get_current_user
from utils.config import settings
from utils.rate_limit import limiter
from services.analyzer import get_data_collector, get_ai_analyzer, DataCollector, AIAnalyzer
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.post(
    "/auth/token", 
    response_model=Token, 
    tags=["authentication"],
    summary="Generate access token",
    description="Exchanges a username and password for a JWT bearer token."
)
@limiter.limit("5/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Generate an access token for user authentication.
    """
    logger.info(f"Token generation requested for user: {form_data.username}")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/analyze/{sector}",
    summary="Analyze trade opportunities",
    description="Collects real-time market data and generates a strategic analysis report.",
    responses={
        200: {
            "description": "Markdown report file",
            "content": {"text/markdown": {}}
        },
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        502: {"model": ErrorResponse, "description": "Bad Gateway (upstream failure)"},
    },
    tags=["analysis"]
)
@limiter.limit("5/minute")
def analyze_sector(
    request: Request,
    sector: str,
    current_user: str = Depends(get_current_user),
    data_collector: DataCollector = Depends(get_data_collector),
    ai_analyzer: AIAnalyzer = Depends(get_ai_analyzer)
):
    """
    Analyze trade opportunities for a specific sector.
    Requires authentication via token (Bearer).
    Returns a markdown report summarizing data.
    """
    logger.info(f"Analysis request by '{current_user}' for sector: {sector}")
    
    # Input validation
    if not sector.strip() or len(sector) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sector must be at least 2 characters."
        )
    
    sector = sector.strip().lower()
    
    try:
        # Step 1: Collect data
        search_data = data_collector.search_market_data(sector)
        
        # Step 2: Analyze data and generate report (handles caching internally)
        report_markdown = ai_analyzer.generate_report(sector, search_data)
        
        # Format filename safely
        safe_filename = "".join([c if c.isalnum() else "_" for c in sector])
        
        return Response(
            content=report_markdown,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f"attachment; filename={safe_filename}_report.md"
            }
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error analyzing {sector}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during analysis."
        )
