from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.schemas.description_schema import (DescriptionRequest, 
                                            DescriptionResponse)

class State(TypedDict):
    messages: List[str]

class DescriptionService:
    SYSTEM_PROMPT = """You are a professional product description writer and editor. Your task is to:
    1. Rewrite the product description given to you as if you are the seller, following the seller's persona.
    2. Improve the clarity and readability of product descriptions.
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
        try:
            # Ensure request is a DescriptionRequest object
            if isinstance(request, dict):
                request = DescriptionRequest(**request)
            
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=float(request.temperature or 0.7))

            # Build the input message
            seller_persona = f"This description is aimed at {request.seller_persona}." if request.seller_persona else ""
            item_condition = f"The item is {request.item_condition}." if request.item_condition else ""
            description = f"{request.description.strip()}"

            input_message = f"{seller_persona} {item_condition} {description}"

            graph_builder = StateGraph(State)

            async def chatbot(state: State):
                messages = [
                    SystemMessage(content=DescriptionService.SYSTEM_PROMPT)
                ] + [HumanMessage(content=msg) for msg in state["messages"]]
                result = await llm.ainvoke(messages)
                return {"messages": [result.content]}
            
            graph_builder.add_node("chatbot", chatbot)
            graph_builder.add_edge(START, "chatbot")
            graph_builder.add_edge("chatbot", END)
            
            graph = graph_builder.compile()
            result = await graph.ainvoke({"messages": [input_message]})
            refined_description = result["messages"][0]

            return DescriptionResponse(
                seller_persona=request.seller_persona,
                refined_description=refined_description
            )
        except Exception as e:
            print(f"Error in LLM processing: {str(e)}")
            if isinstance(request, str):
                return DescriptionResponse(
                    seller_persona=None,
                    refined_description=request
                )
            return DescriptionResponse(
                seller_persona=request.seller_persona if hasattr(request, 'seller_persona') else None,
                refined_description=request.description if hasattr(request, 'description') else str(request)
            )
        

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans and sanitizes input text.
        """
        # Implement text cleaning logic
        pass

    @staticmethod
    def enhance_seo(text: str) -> str:
        """
        Enhances text for SEO purposes.
        """
        # Implement SEO enhancement logic
        pass
