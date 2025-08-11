from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_type = Column(String)  # pdf, docx
    file_size = Column(Integer)
    content = Column(Text)
    
    # Extracted metadata
    agreement_type = Column(String, index=True)  # NDA, MSA, etc.
    governing_law = Column(String, index=True)   # UAE, UK, etc.
    # jurisdiction = Column(String, index=True)     # Specific jurisdiction
    industry = Column(String, index=True)        # Technology, Oil & Gas, etc.
    geography = Column(String, index=True)       # Middle East, Europe, etc.
    
    # Processing metadata
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', agreement_type='{self.agreement_type}')>"
