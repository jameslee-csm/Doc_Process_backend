import json
from typing import Dict, Any
from openai import OpenAI
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

class MetadataExtractor:
    def __init__(self):
        """Initialize the MetadataExtractor with OpenRouter configuration using OpenAI client"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def extract_metadata(self, content: str, filename: str) -> Dict[str, Any]:
        """
        Extract metadata from document content using OpenRouter API.
        
        Args:
            content (str): The text content of the document
            filename (str): Name of the file (used for reference)
            
        Returns:
            Dict[str, Any]: Extracted metadata including agreement_type, governing_law,
                          geography, and industry
        """
        try:
            # Prepare the prompt for the model
            prompt = (
                "Read the content and output JSON with agreement_type, governing_law, "
                "geography, industry. For each field, if the information is not found, "
                "use null.\n\nDocument content:\n" + content
            )

            # Call OpenRouter API using OpenAI client
            response = self.client.chat.completions.create(
                
                model="anthropic/claude-3.7-sonnet:beta",  # Using Claude 3 Sonnet
                messages=[
                    {
                        "role": "system",
                        "content": "You are a legal document analyzer. Extract key metadata from legal agreements and output in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.0  # Use 0 temperature for consistent, deterministic outputs
            )

            # Extract the JSON response
            try:
                # Clean up the response content by removing markdown code block and any whitespace
                content = response.choices[0].message.content
                # Remove markdown code block formatting if present
                content = content.replace('```json', '').replace('```', '').strip()
                
                metadata = json.loads(content)
                
                # Ensure all required fields are present
                required_fields = ['agreement_type', 'governing_law', 'geography', 'industry']
                for field in required_fields:
                    if field not in metadata:
                        metadata[field] = None
                
                return metadata
                # return {
                #     'agreement_type': metadata['agreement_type'],
                #     'governing_law': metadata['governing_law'],
                #     'industry': metadata['industry'],
                #     'geography': metadata['geography']
                # }

            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to parse API response as JSON"
                )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting metadata: {str(e)}"
            )