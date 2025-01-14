# Product Description Refiner API

A FastAPI-based service that refines product descriptions using AI language models and OpenAI's GPT-4.

## Features

- AI-powered product description refinement
- Smart title generation
- Seller persona customization
- Location-aware descriptions
- Condition-specific formatting
- Adjustable creativity settings
- SEO optimization
- Grammar and readability improvements

## Prerequisites

- Python 3.8+
- OpenAI API key

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

# Set up environment variables
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

## Configuration

Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
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
  "description": "iPhone 13 Pro 256GB in perfect condition",
  "seller_persona": "tech-savvy individual",
  "seller_address": "Somerset, NJ",
  "item_condition": "new",
  "temperature": 0.7
}'
```

## API Documentation

### POST /refine/

Refines a product description and generates a title.

**Request Body Schema:**
```json
{
  "description": "string (required)",
  "seller_persona": "string (optional)",
  "seller_address": "string (optional)",
  "item_condition": "string (optional: new|used|refurbished)",
  "temperature": "float (optional, range: 0.0-1.0, default: 0.7)"
}
```

**Response Schema:**
```json
{
  "refined_description": "string",
  "refined_title": "string",
  "seller_persona": "string",
  "item_condition": "string"
}
```

## Development

- Framework: FastAPI
- LLM Integration: LangChain
- Models: GPT-4
- Validation: Pydantic v2

## Error Handling

The API includes comprehensive error handling for:
- Invalid input validation
- Missing API keys
- LLM service interruptions
- Rate limiting

## License

MIT License

## Support

For issues and feature requests, please open an issue on the repository.
