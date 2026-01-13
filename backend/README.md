# Vibe-Coding Backend

Multi-agent AI system for generating React + TypeScript websites.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Create `.env` file:

```bash
cp .env.example .env
```

1. Add your OpenRouter API key to `.env`:

```env
OPENROUTER_API_KEY=your_actual_key_here
```

Get your key from: <https://openrouter.ai/keys>

## Run

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload
```

Backend will run on: <http://localhost:8000>

## API Endpoints

- `POST /api/generate` - Generate website from prompt
- `GET /api/health` - Health check
- `GET /docs` - Interactive API documentation

## Architecture

- **Planner Agent** (DeepSeek R1T2): Creates UX strategy
- **Copywriter Agent** (Gemma 3N): Generates marketing copy
- **Code Agent** (Qwen 3 Coder): Builds React components
- **Aggregator**: Merges all outputs into final result
