from fastapi import FastAPI, HTTPException, Request
from app.schemas.description_schema import DescriptionRequest, DescriptionResponse
from app.services.description_service import DescriptionService

app = FastAPI(title="Product Refiner API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Refiner API"}

@app.post("/refine/", response_model=DescriptionResponse)
async def refine_description(request: DescriptionRequest):
    try:
        # Validate request data
        request_dict = request.model_dump()
        validated_request = DescriptionRequest(**request_dict)
        
        service = DescriptionService()
        refined = await service.refine_description_with_llm(validated_request)
        return refined
    except Exception as e:
        raise HTTPException(
            status_code=422 if "validation" in str(e).lower() else 500,
            detail=str(e)
        )

@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return {"detail": str(exc)}, 422 if "validation" in str(exc).lower() else 500
