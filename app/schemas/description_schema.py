from pydantic import BaseModel, Field, field_validator
from typing import Optional

class DescriptionRequest(BaseModel):
    description: str = Field(
        ...,
        min_length=1,
        description="The original product description to be refined"
    )
    seller_address: str = Field(
        ...,
        min_length=1,
        description="The location of the seller"
    )
    seller_persona: Optional[str] = Field(
        default=None,
        description="The persona or style of the seller"
    )
    item_condition: Optional[str] = Field(
        default=None,
        description="The condition of the item (new, used, refurbished)"
    )
    temperature: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Creativity level for text generation. A value between 0.0 and 1.0, lower for more factual, higher for more creative."
    )

    @field_validator('item_condition')
    def validate_condition(cls, v):
        if v and v.lower() not in ['new', 'used', 'refurbished']:
            raise ValueError('Item condition must be either "new", "used", or "refurbished"')
        return v.lower() if v else None

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Sample description to refine",
                "seller_address": "Somerset, NJ",
                "seller_persona": "tech-savvy individual",
                "item_condition": "new",
                "temperature": 0.7
            }
        }

class DescriptionResponse(BaseModel):
    seller_persona: Optional[str] = Field(
        default=None,
        description="The persona used for refinement"
    )
    refined_description: str = Field(
        ...,
        description="The AI-refined product description"
    )
    refined_title: str = Field(
        ...,
        description="The AI-generated product title"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "seller_persona": "tech-savvy individual",
                "refined_description": "This is a refined description of the product.",
                "refined_title": "Refined Product Title"
            }
        }
