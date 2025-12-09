"""FastAPI application for DocRAG system."""

from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

from src.embed.embedding_model import EmbeddingModel
from src.embed.vector_store import FaissVectorStore
from src.generation.llm_client import OllamaClient
from src.generation.prompt_builder import build_technical_doc_prompt
from src.parse.chunker import chunk_text
from src.parse.pdf_parser import extract_text_from_pdf
from src.parse.text_cleaner import clean_text
from src.retrieval.retriever import Retriever
from src.validation.validator import validate_document

app = FastAPI(title="DocRAG API", description="Technical Document Generation and Validation System")

# Global instances
embed_model: Optional[EmbeddingModel] = None
vector_store: Optional[FaissVectorStore] = None
retriever: Optional[Retriever] = None
llm_client: Optional[OllamaClient] = None


def initialize_components() -> None:
    """Initialize global components."""
    global embed_model, vector_store, retriever, llm_client
    if embed_model is None:
        embed_model = EmbeddingModel()
    if vector_store is None:
        vector_store = FaissVectorStore(dimension=384)
    if retriever is None:
        retriever = Retriever(embed_model, vector_store)
    if llm_client is None:
        llm_client = OllamaClient()


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize components on startup."""
    initialize_components()


class GenerateRequest(BaseModel):
    """Request model for document generation."""

    query: str


class GenerateResponse(BaseModel):
    """Response model for document generation."""

    document: str
    validation: dict


class ValidateRequest(BaseModel):
    """Request model for document validation."""

    text: str


class ValidateResponse(BaseModel):
    """Response model for document validation."""

    validation: dict


class IndexResponse(BaseModel):
    """Response model for document indexing."""

    message: str
    chunks_count: int


@app.get("/")
def root() -> dict:
    """Root endpoint."""
    return {"message": "DocRAG API", "status": "running"}


@app.post("/index", response_model=IndexResponse)
async def index_document(file: UploadFile = File(...)) -> IndexResponse:
    """Index a new document (PDF) for retrieval."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        # Save uploaded file temporarily
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # Parse PDF
            raw_text = extract_text_from_pdf(tmp_path)
            cleaned_text = clean_text(raw_text)
            chunks = chunk_text(cleaned_text, max_tokens=300, overlap=50)

            # Initialize components if needed
            initialize_components()

            # Generate embeddings
            embeddings = embed_model.embed(chunks)
            dimension = embeddings.shape[1]

            # Initialize or update vector store if needed
            global vector_store, retriever
            if vector_store is None or vector_store.index.index.ntotal == 0:
                vector_store = FaissVectorStore(dimension=dimension)
                retriever = Retriever(embed_model, vector_store)

            # Check dimension compatibility
            if vector_store.index.dimension != dimension:
                raise HTTPException(
                    status_code=400,
                    detail=f"Embedding dimension mismatch. Expected {vector_store.index.dimension}, got {dimension}",
                )

            # Add embeddings to store
            vector_store.add(embeddings, chunks)

            return IndexResponse(
                message=f"Document '{file.filename}' indexed successfully",
                chunks_count=len(chunks),
            )
        finally:
            os.unlink(tmp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing document: {str(e)}")


@app.post("/validate", response_model=ValidateResponse)
def validate_text(request: ValidateRequest) -> ValidateResponse:
    """Validate a provided text document."""
    report = validate_document(request.text)
    return ValidateResponse(validation=report)


@app.post("/generate", response_model=GenerateResponse)
def generate_doc(request: GenerateRequest) -> GenerateResponse:
    """Generate and validate a technical document."""
    initialize_components()

    if retriever is None or vector_store is None:
        raise HTTPException(
            status_code=400,
            detail="No documents indexed. Please index a document first using /index",
        )

    if vector_store.index.index.ntotal == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents indexed. Please index a document first using /index",
        )

    try:
        # Retrieve relevant contexts
        contexts: List[str] = retriever.retrieve(request.query, k=5)

        # Build prompt
        prompt = build_technical_doc_prompt(request.query, contexts)

        # Generate document with LLM
        doc = llm_client.generate(prompt)

        # Validate document
        report = validate_document(doc)

        return GenerateResponse(document=doc, validation=report)

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Ollama not found. Please install Ollama and ensure it's in your PATH.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")

