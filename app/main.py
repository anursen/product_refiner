from fastapi import FastAPI, HTTPException
from app.schemas.description_schema import DescriptionRequest, DescriptionResponse
from app.services.description_service import DescriptionService

app = FastAPI(title="Product Refiner API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Refiner API"}

@app.post("/refine/", response_model=DescriptionResponse)
async def refine_description(request: DescriptionRequest):
    try:
        service = DescriptionService()
        refined = await service.refine_description_with_llm(request)
        
        # Return the response directly since service already returns DescriptionResponse
        return refined
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
