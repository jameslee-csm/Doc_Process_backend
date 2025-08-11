import re
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class MetadataExtractor:
    """Extract metadata from legal documents using pattern matching"""
    
    def __init__(self):
        # Agreement type patterns
        self.agreement_patterns = {
            'NDA': r'\b(?:NDA|Non-Disclosure Agreement|Non Disclosure Agreement)\b',
            'MSA': r'\b(?:MSA|Master Service Agreement|Master Services Agreement)\b',
            'Franchise Agreement': r'\b(?:Franchise Agreement|Franchising Agreement)\b',
            'Employment Agreement': r'\b(?:Employment Agreement|Employment Contract)\b',
            'License Agreement': r'\b(?:License Agreement|Licensing Agreement)\b',
            'Service Agreement': r'\b(?:Service Agreement|Services Agreement)\b',
            'Purchase Agreement': r'\b(?:Purchase Agreement|Purchase Contract)\b',
            'Lease Agreement': r'\b(?:Lease Agreement|Leasing Agreement)\b'
        }
        
        # Jurisdiction patterns
        self.jurisdiction_patterns = {
            'UAE': r'\b(?:UAE|United Arab Emirates|Dubai|Abu Dhabi|Sharjah)\b',
            'UK': r'\b(?:UK|United Kingdom|England|Wales|Scotland|Northern Ireland)\b',
            'US': r'\b(?:US|USA|United States|Delaware|New York|California)\b',
            'Singapore': r'\b(?:Singapore|SG)\b',
            'Hong Kong': r'\b(?:Hong Kong|HK)\b',
            'Qatar': r'\b(?:Qatar|Doha)\b',
            'Saudi Arabia': r'\b(?:Saudi Arabia|KSA|Riyadh)\b',
            'Kuwait': r'\b(?:Kuwait|Kuwait City)\b',
            'Bahrain': r'\b(?:Bahrain|Manama)\b',
            'Oman': r'\b(?:Oman|Muscat)\b'
        }
        
        # Industry patterns
        self.industry_patterns = {
            'Technology': r'\b(?:technology|software|IT|digital|cyber|AI|artificial intelligence|machine learning)\b',
            'Oil & Gas': r'\b(?:oil|gas|petroleum|energy|drilling|exploration|refinery)\b',
            'Healthcare': r'\b(?:healthcare|medical|pharmaceutical|biotech|hospital|clinic|medicine)\b',
            'Finance': r'\b(?:finance|banking|investment|financial|capital|fund|asset)\b',
            'Real Estate': r'\b(?:real estate|property|construction|development|building|land)\b',
            'Manufacturing': r'\b(?:manufacturing|production|factory|industrial|machinery)\b',
            'Retail': r'\b(?:retail|commerce|e-commerce|shopping|store|merchandise)\b',
            'Transportation': r'\b(?:transportation|logistics|shipping|freight|delivery|warehouse)\b'
        }
        
        # Geography patterns
        self.geography_patterns = {
            'Middle East': r'\b(?:Middle East|Gulf|GCC|Arabian Peninsula|Persian Gulf)\b',
            'Europe': r'\b(?:Europe|European|EU|European Union)\b',
            'Asia': r'\b(?:Asia|Asian|Asia-Pacific|APAC)\b',
            'North America': r'\b(?:North America|American|USA|Canada)\b',
            'Africa': r'\b(?:Africa|African)\b',
            'Australia': r'\b(?:Australia|Australian|Oceania)\b'
        }
    
    def extract_metadata(self, content: str, filename: str) -> Dict[str, Optional[str]]:
        """Extract all metadata from document content"""
        try:
            # Convert to lowercase for case-insensitive matching
            content_lower = content.lower()
            
            # Extract agreement type
            agreement_type = self._extract_agreement_type(content_lower, filename)
            
            # Extract jurisdiction
            jurisdiction = self._extract_jurisdiction(content_lower)
            
            # Extract industry
            industry = self._extract_industry(content_lower)
            
            # Extract geography
            geography = self._extract_geography(content_lower)
            
            # Extract governing law (same as jurisdiction for now)
            governing_law = jurisdiction
            
            return {
                'agreement_type': agreement_type,
                'governing_law': governing_law,
                'jurisdiction': jurisdiction,
                'industry': industry,
                'geography': geography
            }
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {
                'agreement_type': None,
                'governing_law': None,
                'jurisdiction': None,
                'industry': None,
                'geography': None
            }
    
    def _extract_agreement_type(self, content: str, filename: str) -> Optional[str]:
        """Extract agreement type from content and filename"""
        # Check filename first
        filename_lower = filename.lower()
        for agreement_type, pattern in self.agreement_patterns.items():
            if re.search(pattern, filename_lower, re.IGNORECASE):
                return agreement_type
        
        # Check content
        for agreement_type, pattern in self.agreement_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                return agreement_type
        
        return None
    
    def _extract_jurisdiction(self, content: str) -> Optional[str]:
        """Extract jurisdiction from content"""
        for jurisdiction, pattern in self.jurisdiction_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                return jurisdiction
        return None
    
    def _extract_industry(self, content: str) -> Optional[str]:
        """Extract industry from content"""
        for industry, pattern in self.industry_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                return industry
        return None
    
    def _extract_geography(self, content: str) -> Optional[str]:
        """Extract geography from content"""
        for geography, pattern in self.geography_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                return geography
        return None
