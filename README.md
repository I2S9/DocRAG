# DocRAG - Technical Document Generation and Compliance System

A production-ready RAG (Retrieval-Augmented Generation) system for generating and validating technical documentation. The system ingests technical source documents, extracts their structure, and generates new technical documents that follow predefined formats with automated validation and compliance checking.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Requirements](#requirements)

## Features

- **Document Parsing**: Extract and clean text from PDF files
- **Intelligent Chunking**: Split documents into manageable chunks with overlap
- **Semantic Search**: FAISS-based vector storage and retrieval
- **Document Generation**: LLM-powered technical document generation using Ollama
- **Automated Validation**: Check document completeness and structural compliance
- **PDF Export**: Generate formatted PDF documents and validation reports
- **RESTful API**: FastAPI-based backend with comprehensive endpoints
- **Web Interface**: Streamlit-based UI for easy interaction

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
DocRAG/
├── src/
│   ├── parse/          # Document parsing and chunking
│   ├── embed/           # Embedding generation and FAISS indexing
│   ├── retrieval/       # RAG retrieval system
│   ├── generation/      # LLM integration and prompt building
│   ├── validation/      # Document validation and compliance checking
│   ├── api/             # FastAPI REST endpoints
│   ├── ui/              # Streamlit web interface
│   └── utils/           # Utility functions (PDF export, etc.)
├── models/              # Model storage
├── docs/                # Documentation and example documents
├── data/                # Data storage (gitignored)
└── tests/               # Unit and integration tests
```

### Pipeline Flow

1. **Document Ingestion**: PDF files are parsed and cleaned
2. **Chunking**: Text is split into overlapping chunks
3. **Embedding**: Chunks are converted to vectors using sentence-transformers
4. **Indexing**: Vectors are stored in FAISS for efficient retrieval
5. **Retrieval**: Query-based semantic search retrieves relevant chunks
6. **Generation**: LLM generates documents based on retrieved context
7. **Validation**: Generated documents are checked for completeness and compliance
8. **Export**: Documents and reports can be exported as PDF

## Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed and configured (for LLM generation)
  - Download from: https://ollama.ai/
  - Install and ensure it's in your PATH
  - Pull a model: `ollama pull llama3`

### Setup

1. Clone the repository:
```bash
git clone https://github.com/I2S9/DocRAG.git
cd DocRAG
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python -m src.main
```

## Usage

### Quick Start

**Start the API server:**
```bash
python start_api.py
# Or: uvicorn src.api.app:app --reload
```
API available at `http://localhost:8000`

**Start the web interface (in a separate terminal):**
```bash
python run_ui.py
# Or: streamlit run src/ui/app.py
```
Interface available at `http://localhost:8501`

### Workflow

1. Upload a PDF document through the web interface
2. Enter a generation query (e.g., "Generate a technical specification for component X")
3. Review the generated document and validation report
4. Export documents or reports as PDF if needed

## API Endpoints

### GET `/`
Root endpoint returning API status.

### POST `/index`
Index a PDF document for retrieval.

**Request**: Multipart form data with PDF file
**Response**: 
```json
{
  "message": "Document 'filename.pdf' indexed successfully",
  "chunks_count": 33
}
```

### POST `/generate`
Generate a technical document based on a query.

**Request**:
```json
{
  "query": "Generate a technical specification for component X"
}
```

**Response**:
```json
{
  "document": "Generated document text...",
  "validation": {
    "all_sections_present": true,
    "sections": {
      "Introduction": true,
      "Scope": true,
      "Requirements": true,
      "Constraints": true,
      "Safety considerations": true
    }
  }
}
```

### POST `/validate`
Validate a document's structure and completeness.

**Request**:
```json
{
  "text": "Document text to validate..."
}
```

**Response**:
```json
{
  "validation": {
    "all_sections_present": false,
    "sections": {
      "Introduction": true,
      "Scope": true,
      "Requirements": false,
      "Constraints": false,
      "Safety considerations": false
    }
  }
}
```

### POST `/export`
Export a document or validation report to PDF.

**Request**:
```json
{
  "text": "Document text to export...",
  "title": "Technical Document",
  "export_type": "document"
}
```

**Response**: PDF file download


## Testing

Run unit tests:

```bash
python -m pytest tests/test_unit_*.py -v
```

Run integration tests (requires PDF files in `docs/` directory):

```bash
python tests/test_parsing.py
python tests/test_validation.py
```

## Requirements

### Required Sections for Technical Documents

The validation system checks for the following required sections:

- Introduction
- Scope
- Requirements
- Constraints
- Safety considerations

### Model Requirements

- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (default, ~80MB)
- **LLM**: Ollama with a compatible model (e.g., `llama3`, `llama3:8b`)

### System Requirements

- Minimum 4GB RAM (8GB recommended)
- Python 3.8+
- Ollama installed and configured
- Internet connection for initial model downloads

## Limitations

- PDF parsing quality depends on PDF structure
- LLM generation speed depends on hardware and model size
- Validation rules are configurable but currently fixed
- FAISS index is in-memory (not persisted between restarts)