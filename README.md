# Product Description Refiner API

A FastAPI-based service that refines product descriptions using AI language models.

## Features

- Refine product descriptions using GPT-4
- Customize output based on seller persona
- Support for different item conditions
- Adjustable creativity with temperature control
- SEO optimization
- Grammar and readability improvements

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd product_refiner

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python run.py
```

2. The API will be available at `http://127.0.0.1:8000`

3. Example API call:
```bash
curl -X POST "http://127.0.0.1:8000/refine/" \
-H "Content-Type: application/json" \
-d '{
  "description": "Sample product description",
  "seller_persona": "tech-savvy individual",
  "item_condition": "new",
  "temperature": 0.7
}'
```

## API Endpoints

### POST /refine/

Refines a product description.

**Request Body:**
```json
{
  "description": "string",
  "seller_persona": "string (optional)",
  "item_condition": "string (optional)",
  "temperature": "float (optional, default: 0.7)"
}
```

**Response:**
```json
{
  "seller_persona": "string",
  "refined_description": "string"
}
```

## Development

- Built with FastAPI
- Uses LangChain for LLM integration
- Implements async processing with LangGraph
- Pydantic models for request/response validation

## License

MIT License
