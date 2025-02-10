from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.description_schema import DescriptionRequest, DescriptionResponse
from app.services.description_service import DescriptionService
import logging
from fastapi.responses import JSONResponse  # added import
from fastapi.templating import Jinja2Templates

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Product Refiner API")

templates = Jinja2Templates(directory="app/templates")  # No extra indent here

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Product Refiner API"}

@app.post("/refine")  # Remove trailing slash
async def refine_description(request: DescriptionRequest) -> DescriptionResponse:
    logger.info(f"Received request: {request.json()}")
    try:
        service = DescriptionService()
        refined = await service.refine_description_with_llm(request)
        logger.info(f"Returning response: {refined.json() if hasattr(refined, 'json') else refined}")
        return refined
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/ui")
async def ui_form(request: Request):
    return templates.TemplateResponse("ui.html", {"request": request})

@app.post("/ui")
async def ui_submit(
    request: Request,
    description: str = Form(...),
    seller_address: str = Form(None),
    seller_persona: str = Form(None),
    item_condition: str = Form(None),
    temperature: float = Form(0.7),
    custom_prompt: str = Form(None),
    custom_model: str = Form(None)
):
    req_data = {
        "description": description,
        "seller_address": seller_address,
        "seller_persona": seller_persona,
        "item_condition": item_condition,
        "temperature": temperature,
        "custom_prompt": custom_prompt,
        "custom_model": custom_model
    }
    logger.info(f"Received UI form data: {req_data}")
    try:
        service = DescriptionService()
        refined = await service.refine_description_with_llm(req_data)
        logger.info(f"Returning refined response from UI: {refined.json() if hasattr(refined, 'json') else refined}")
        return templates.TemplateResponse("ui.html", {"request": request, "result": refined.dict()})
    except Exception as e:
        logger.error(f"Error processing UI form: {str(e)}")
        return templates.TemplateResponse("ui.html", {"request": request, "error": str(e)})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": str(exc)})  # updated response
