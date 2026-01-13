# Vibe-Coding - Complete Setup Guide

## Project Overview

Multi-agent AI coding tool that uses 3 specialized AI models to generate premium React + TypeScript websites.

## Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_key_here
```

Get your key from: <https://openrouter.ai/keys>

Start backend:

```bash
python main.py
```

Backend runs on: <http://localhost:8000>

### 2. Frontend Setup

```bash
npm install
npm run dev
```

Frontend runs on: <http://localhost:5173>

## Usage

1. Open <http://localhost:5173>
2. Click "Get Started"
3. Enter your website description
4. Watch 3 AI agents work in parallel
5. Download the generated code

## Architecture

### Multi-Agent System

- 🧠 **Planner Agent** (DeepSeek R1T2) - Architecture & UX
- ✍️ **Copywriter Agent** (Gemma 3N) - Marketing copy
- ⚡ **Code Agent** (Qwen 3 Coder) - React components

### Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: React + TypeScript + Vite
- **AI**: OpenRouter API (free models)

## Project Structure

```
vibe-coder/
├── backend/
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── copywriter_agent.py
│   │   └── code_agent.py
│   ├── routes/
│   │   └── generate.py
│   ├── aggregator.py
│   ├── openrouter_client.py
│   └── main.py
├── src/
│   ├── components/
│   │   ├── Hero.tsx
│   │   ├── Features.tsx
│   │   ├── ToolInterface.tsx
│   │   ├── PromptInput.tsx
│   │   ├── AgentPanel.tsx
│   │   └── CodePreview.tsx
│   ├── App.tsx
│   └── index.css
└── README.md
```
