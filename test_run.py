#!/usr/bin/env python3
"""
Simple test script to verify backend functionality
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.metadata_extractor import MetadataExtractor
from app.services.query_service import QueryService

def test_metadata_extraction():
    """Test metadata extraction functionality"""
    print("Testing metadata extraction...")
    
    extractor = MetadataExtractor()
    
    # Test cases
    test_cases = [
        {
            'content': 'This is a Non-Disclosure Agreement between parties.',
            'filename': 'nda_contract.pdf',
            'expected_type': 'NDA'
        },
        {
            'content': 'Master Service Agreement terms and conditions.',
            'filename': 'service_contract.docx',
            'expected_type': 'MSA'
        },
        {
            'content': 'This agreement is governed by UAE law and Dubai courts.',
            'filename': 'contract.pdf',
            'expected_jurisdiction': 'UAE'
        },
        {
            'content': 'Software development and technology services agreement.',
            'filename': 'tech_contract.pdf',
            'expected_industry': 'Technology'
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        metadata = extractor.extract_metadata(test_case['content'], test_case['filename'])
        
        print(f"Test {i+1}:")
        print(f"  Content: {test_case['content'][:50]}...")
        print(f"  Filename: {test_case['filename']}")
        print(f"  Extracted metadata: {metadata}")
        
        if 'expected_type' in test_case:
            assert metadata['agreement_type'] == test_case['expected_type'], f"Expected {test_case['expected_type']}, got {metadata['agreement_type']}"
        
        if 'expected_jurisdiction' in test_case:
            assert metadata['jurisdiction'] == test_case['expected_jurisdiction'], f"Expected {test_case['expected_jurisdiction']}, got {metadata['jurisdiction']}"
        
        if 'expected_industry' in test_case:
            assert metadata['industry'] == test_case['expected_industry'], f"Expected {test_case['expected_industry']}, got {metadata['industry']}"
        
        print("  ✓ PASSED")
        print()

def test_query_service():
    """Test query service functionality"""
    print("Testing query service...")
    
    query_service = QueryService()
    
    # Test cases
    test_cases = [
        {
            'question': 'Which agreements are governed by UAE law?',
            'expected_type': 'jurisdiction'
        },
        {
            'question': 'Show me all NDA contracts',
            'expected_type': 'agreement_type'
        },
        {
            'question': 'Find technology industry agreements',
            'expected_type': 'industry'
        },
        {
            'question': 'What contracts do we have?',
            'expected_type': 'general'
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        query_type = query_service._determine_query_type(test_case['question'])
        
        print(f"Test {i+1}:")
        print(f"  Question: {test_case['question']}")
        print(f"  Detected type: {query_type}")
        print(f"  Expected type: {test_case['expected_type']}")
        
        assert query_type == test_case['expected_type'], f"Expected {test_case['expected_type']}, got {query_type}"
        
        print("  ✓ PASSED")
        print()

def main():
    """Run all tests"""
    print("Running backend tests...")
    print("=" * 50)
    
    try:
        test_metadata_extraction()
        test_query_service()
        
        print("=" * 50)
        print("✓ All tests passed!")
        print("\nBackend is ready to run with: uvicorn main:app --reload")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
