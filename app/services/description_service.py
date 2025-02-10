from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from app.schemas.description_schema import (DescriptionRequest, 
                                            DescriptionResponse)
from langchain_core.output_parsers import PydanticOutputParser



class DescriptionService:
    SYSTEM_PROMPT = """You are a professional product description writer and editor. Your task is to:
    Generate a listing for a given product below. 
Include:
- A description highlighting its features
- Try to stick to the original description, Dont make up any related with product spec or features.
Return the output in the format_instructions JSON format:
"""
    @staticmethod
    async def refine_description_with_llm(request: DescriptionRequest) -> DescriptionResponse:
        try:
            # Ensure request is a DescriptionRequest object
            if isinstance(request, dict):
                request = DescriptionRequest(**request)
            parser = PydanticOutputParser(pydantic_object=DescriptionResponse)
            model_name = request.custom_model if request.custom_model else "gpt-4o-mini"
            model = ChatOpenAI(
                model=model_name,
                temperature=float(request.temperature or 0.7)
            )
            # Use custom prompt if provided
            system_prompt = request.custom_prompt if request.custom_prompt else DescriptionService.SYSTEM_PROMPT
            seller_persona = f"You need to write this description from the mouth of {request.seller_persona}." if request.seller_persona else ""
            item_condition = f"The item is {request.item_condition}." if request.item_condition else ""
            seller_address = f"The seller is located in {request.seller_address}." if request.seller_address else ""
            description = f"{request.description.strip()}"
            prompt_template = f"""
            {system_prompt}
            - format_instructions: {parser.get_format_instructions()},
            Product Information:
            - Description: {description}
            - Seller: {seller_persona}
            - Condition: {item_condition}
            - Location: {seller_address}
            """
            messages = [SystemMessage(content=prompt_template)]
            output = await model.ainvoke(messages)
            refined_output = output.content
            # Parse the raw output into a valid JSON object
            refined_response = parser.parse(refined_output)
            # Log the parsed response if needed
            print(f"Parsed response: {refined_response}")
            return refined_response
        except Exception as e:
            raise Exception(f"Error in description refinement: {str(e)}")
    async def parse_output(self, product_name: str) -> List[dict]:
        return