from pydantic import BaseModel, Field

class Token(BaseModel):
    """Schema for the authentication token response."""
    access_token: str = Field(..., description="The JWT access token", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(..., description="The type of the token, typically 'bearer'", example="bearer")
    
class ErrorResponse(BaseModel):
    """Schema for standard error responses."""
    detail: str = Field(..., description="Detailed error message explaining what went wrong", example="Could not validate credentials")
