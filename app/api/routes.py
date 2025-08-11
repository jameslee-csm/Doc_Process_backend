from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from ..models.database import get_db, init_db
from ..services.document_service import DocumentService
from ..services.query_service import QueryService

router = APIRouter()

# Initialize database
init_db()

# Pydantic models for request/response
class QueryRequest(BaseModel):
    question: str

class UploadResponse(BaseModel):
    message: str
    processed: int
    failed: int

class DashboardResponse(BaseModel):
    agreement_types: dict
    jurisdictions: dict
    industries: dict

# Initialize services
document_service = DocumentService()
query_service = QueryService()

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload multiple legal documents"""
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Process uploaded files
        result = await document_service.process_upload(files, db)
        
        return UploadResponse(
            message="Documents uploaded successfully",
            processed=result["processed"],
            failed=result["failed"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/query")
async def query_documents(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """Query documents using natural language"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Process query
        results = query_service.process_query(request.question, db)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard_data(db: Session = Depends(get_db)):
    """Get dashboard analytics data"""
    try:
        # Get all documents
        documents = document_service.get_all_documents(db)
        
        # Aggregate data
        agreement_types = {}
        jurisdictions = {}
        industries = {}
        
        for doc in documents:
            # Count agreement types
            if doc.agreement_type:
                agreement_types[doc.agreement_type] = agreement_types.get(doc.agreement_type, 0) + 1
            
            # Count jurisdictions
            if doc.jurisdiction:
                jurisdictions[doc.jurisdiction] = jurisdictions.get(doc.jurisdiction, 0) + 1
            
            # Count industries
            if doc.industry:
                industries[doc.industry] = industries.get(doc.industry, 0) + 1
        
        return DashboardResponse(
            agreement_types=agreement_types,
            jurisdictions=jurisdictions,
            industries=industries
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard data failed: {str(e)}")

@router.get("/documents")
async def get_documents(db: Session = Depends(get_db)):
    """Get all documents (for debugging)"""
    try:
        documents = document_service.get_all_documents(db)
        
        return [
            {
                "id": doc.id,
                "filename": doc.filename,
                "agreement_type": doc.agreement_type,
                "jurisdiction": doc.jurisdiction,
                "industry": doc.industry,
                "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None
            }
            for doc in documents
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get documents: {str(e)}")
