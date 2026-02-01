# KNOWLEDGE ENGINE

> **Upload your brain. Ask questions. Understand everything.**

A high-performance **Personal Knowledge Management (PKM)** system powered by **RAG (Retrieval-Augmented Generation)**. Turn your static PDFs and notes into a queryable, interactive, and visual knowledge base.

### Website Link: https://knowledge-engine-zeta.vercel.app/

## key Features

*   **Fast Batch Uploads**: Drag & drop multiple PDFs/Text files. Processed instantly using parallel batch embeddings.
*   **Neural Chat**: Ask questions about your documents ("What is string theory?"). The AI understands context and favors your **most recent uploads** for relevance.
*   **Semantic Search**: Find concepts, not just keywords. Uses `pgvector` for deep semantic understanding.
*   **Knowledge Graph**: Visualize connections between your notes in a 3D-force graph.
*   **Study Mode**: Automatically generate **Flashcards** from your notes to master new topics.
*   **Persistent Dashboard**: Switch seamlessly between Upload, Search, Chat, and Graph views without losing context.

## Tech Stack

### Core
*   **Language**: Python 3.11+, TypeScript
*   **Database**: PostgreSQL + `pgvector` (Vector Database)
*   **Containerization**: Docker & Docker Compose

### Backend (`/backend`)
*   **Framework**: FastAPI (Async)
*   **ORM**: SQLModel (SQLAlchemy)
*   **ML/AI**:
    *   `sentence-transformers` (all-MiniLM-L6-v2) for Embeddings
    *   `openai` / OpenRouter for LLM Inference
    *   `pypdf` for text extraction

### Frontend (`/frontend`)
*   **Framework**: Next.js 14 (App Router)
*   **Styling**: Tailwind CSS
*   **Icons**: Lucide React
*   **State**: React Hooks (State Persistence)

## Quick Start

### Prerequisites
*   Docker & Docker Compose
*   Node.js 18+
*   Python 3.11+

### 1. Start the Stack
We provide a unified startup script.

```bash
# Clone the repo
git clone https://github.com/yourusername/knowledge-engine.git
cd knowledge-engine

# Run the startup script (Starts DB, Backend, and Frontend)
./start_app.sh
```

### 2. Manual Setup (Alternative)

**Database**
```bash
docker-compose up -d
```

**Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```
