from pydantic import BaseModel, Field
from typing import Optional

class DescriptionRequest(BaseModel):
    description: str = Field(..., min_length=1)
    seller_persona: Optional[str] = Field(default=None)
    item_condition: Optional[str] = Field(default=None)
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=1.0)

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Sample description to refine",
                "seller_persona": "tech-savvy individual",
                "item_condition": "new",
                "temperature": 0.7
            }
        }

class DescriptionResponse(BaseModel):
    seller_persona: Optional[str] = Field(default=None)
    refined_description: str = Field(...)

