from pydantic import BaseModel, Field, field_validator
from typing import Optional
from pydantic import BaseModel, Field

class SimilarProduct(BaseModel):
    item_name: str
    description: str
    price: float
    class Config:
        json_schema_extra = {
            "example": {
                "item_name": "Similar Product",
                "description": "Description of similar product",
                "price": 100.0
            }
        }

class DescriptionRequest(BaseModel):
    description: str = Field(
        ...,
        min_length=1,
        description="The original product description to be refined"
    )
    seller_address: Optional[str] = Field(
        default="Somerset, NJ",  # default set for API requests
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
    similar_products: Optional[list[SimilarProduct]] = Field(
        default=None,
        description="A list of similar products"
    )
    custom_prompt: Optional[str] = Field(
        default="Write a friendly product description:",  # default set for API requests
        description="Custom prompt to override the default system prompt"
    )
    custom_model: Optional[str] = Field(
        default="gpt-4o-mini",  # default set for API requests
        description="Custom model name to override the default model"
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
                "seller_persona": "tech savvy seller",
                "item_condition": "new",
                "temperature": 0.7,
                "custom_prompt": "Write a friendly product description:",
                "custom_model": "gpt-4o-mini"
            }
        }

class DescriptionResponse(BaseModel):
    product_title: Optional[str] = Field(
        default=None,
        description="The AI-generated product title",
        max_length=50
    )
    product_description: str = Field(
        ...,
        description="The AI-refined product description"
    )
    price: Optional[float] = Field(
        default=None,
        description="The AI-generated price for the product"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "product_title": "Refined Product Title",
                "product_description": "This is a refined description of the product.",
                "price": 99.99
            }
        }
