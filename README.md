# SHL Product Catalog Assistant

A FastAPI-based conversational AI assistant that helps users discover and compare SHL (Saville and Holdsworth Limited) assessments and products. The system uses semantic search, intelligent ranking, and safety guardrails to provide accurate product recommendations.

## Features

- 🤖 **Conversational Interface**: Natural language chat for product discovery
- 🔍 **Semantic Search**: FAISS-powered vector search for accurate product retrieval
- 📊 **Smart Ranking**: Rank and filter products based on user needs
- 🔄 **Product Comparison**: Compare multiple SHL assessments side-by-side
- 🛡️ **Safety Guardrails**: Prevent off-topic questions and legal/regulatory issues
- 💾 **Multi-turn Conversations**: Maintain context across conversation history

## Project Structure

```
.
├── app/
│   ├── main.py              # Application entry point
│   ├── routes.py            # FastAPI endpoints
│   ├── models.py            # Pydantic data models
│   ├── retriever.py         # FAISS-based semantic search
│   ├── parser.py            # Query parsing and intent detection
│   ├── ranker.py            # Product ranking and filtering
│   ├── guardrails.py        # Safety and policy enforcement
│   ├── llm.py               # LLM integration
│   └── prompts.py           # Prompt templates
├── data/
│   └── faiss.index          # Pre-built FAISS index for semantic search
├── scripts/
│   └── build_index.py       # Script to build/rebuild FAISS index
├── sample_conversations/    # Sample conversation examples
├── shl_product_catalog.json # Product catalog database
└── requirements.txt         # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8+
- pip or conda

### Setup

1. **Clone or download the repository**

   ```bash
   cd SHL
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify FAISS index**
   ```bash
   python scripts/build_index.py  # Rebuild if needed
   ```

## Usage

### Running the Application

Start the FastAPI server:

```bash
python app/main.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Health Check

```bash
GET /health
```

Returns: `{"status": "ok"}`

#### Chat Endpoint

```bash
POST /chat
```

**Request Body:**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What SHL assessments are best for graduate hiring?"
    }
  ]
}
```

**Response:**

```json
{
  "content": "Here are the recommended SHL assessments...",
  "reasoning": "Based on your query about graduate hiring..."
}
```

### Example Usage

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Can you recommend assessments for technical roles?"}
    ]
  }'
```

## Key Components

### Retriever (`retriever.py`)

- Loads product catalog from `shl_product_catalog.json`
- Uses FAISS for efficient semantic search
- Employs sentence transformers for text embeddings

### Parser (`parser.py`)

- Extracts intent from user queries
- Detects comparison requests
- Generates clarification questions
- Identifies finalizing messages

### Ranker (`ranker.py`)

- Ranks retrieved products by relevance
- Filters based on user requirements
- Generates product recommendations
- Compares multiple items

### Guardrails (`guardrails.py`)

- Blocks off-topic questions
- Enforces legal/regulatory policies
- Provides appropriate refusal responses

## Sample Conversations

Example conversations are provided in `sample_conversations/GenAI_SampleConversations/` (C1.md through C10.md). These demonstrate:

- Various user intents and use cases
- Expected assistant responses
- Multi-turn conversation flow

## Building the Index

To rebuild the FAISS index (required after updating `shl_product_catalog.json`):

```bash
python scripts/build_index.py
```

This script:

1. Reads the product catalog
2. Generates embeddings using sentence transformers
3. Creates a FAISS index
4. Saves the index to `data/faiss.index`

## Configuration

### Environment Variables

- `FAISS_INDEX_PATH`: Path to FAISS index (default: `data/faiss.index`)
- `CATALOG_PATH`: Path to product catalog (default: `shl_product_catalog.json`)

### Customization

- **Models**: Edit `app/models.py` to modify request/response schemas
- **Prompts**: Update `app/prompts.py` for custom LLM prompts
- **Safety Rules**: Modify `app/guardrails.py` to adjust policies

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **sentence-transformers**: Text embeddings
- **faiss-cpu**: Vector similarity search
- **pydantic**: Data validation
- **requests**: HTTP client
- **beautifulsoup4**: HTML parsing
- **pandas**: Data manipulation
- **numpy**: Numerical computing

See `requirements.txt` for versions.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Structure Best Practices

- Keep route handlers in `routes.py` thin
- Use `models.py` for all data validation
- Centralize prompts in `prompts.py`
- Add safety checks in `guardrails.py`

## Troubleshooting

### FAISS Index Not Found

```bash
python scripts/build_index.py
```

### Run main app

```bash
python app/main.py 
```
