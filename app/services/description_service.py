from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from app.schemas.description_schema import (DescriptionRequest, 
                                            DescriptionResponse)

class State(TypedDict):
    messages: List[str]

class DescriptionService:
    SYSTEM_PROMPT = """You are a professional product description writer and editor. Your task is to:
    1. Rewrite the product description given to you as if you are the seller, following the seller's persona.
    2. Improve the clarity and readability of product descriptions.
    3. Include seller information to the listing.
    3. Ensure proper grammar and punctuation.
    4. Optimize for SEO while maintaining natural language.
    5. Highlight key product features and benefits.
    6. Maintain a professional and engaging tone as if you are speaking as the seller's persona.
    7. Explicitly incorporate the item condition (e.g., new, used, refurbished) into the description.
    8. Strictly adhere to the provided product specifications—do not invent features or details.
    9. Adjust the level of creativity based on the provided temperature value.
    Please refine the given product description while preserving all factual information."""

    @staticmethod
    async def refine_description_with_llm(request: DescriptionRequest) -> DescriptionResponse:
        """
        Refines the product description using LLM.
        """
        
        # Ensure request is a DescriptionRequest object
        if isinstance(request, dict):
                request = DescriptionRequest(**request)
            
        llm = ChatOpenAI(model="gpt-4", temperature=float(request.temperature or 0.7))
        # Build the input message
        seller_persona = f"This description is aimed at {request.seller_persona}." if request.seller_persona else ""
        item_condition = f"The item is {request.item_condition}." if request.item_condition else ""
        seller_address = f"The seller is located in {request.seller_address}." if request.seller_address else ""
        description = f"{request.description.strip()}"
        prompt_template = f"""
        {DescriptionService.SYSTEM_PROMPT}
        
        
        Product Information:
        - Description: {description}
        - Seller: {seller_persona}
        - Condition: {item_condition}
        - Location: {seller_address}
        """

        messages = [SystemMessage(content=prompt_template)]
        output = await llm.ainvoke(messages)
        
        # Extract the content from the AIMessage
        refined_description = output.content if hasattr(output, 'content') else str(output)
        
        return DescriptionResponse(
            refined_description=refined_description,  
            refined_title=f"Refined {request.item_condition} Product", 
            seller_persona=request.seller_persona,
            item_condition=request.item_condition
        )