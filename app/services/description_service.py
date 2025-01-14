from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from app.schemas.description_schema import (DescriptionRequest, 
                                            DescriptionResponse)

class State(TypedDict):
    messages: List[str]

class DescriptionService:
    SYSTEM_PROMPT = """You are a professional product description writer and editor. Your task is to:
    Generate a listing for a given product. 
Include:
- A catchy title
- A description highlighting its features
- A competitive price
- Suggested categories for Facebook Marketplace
- Dont Change the original description"""

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