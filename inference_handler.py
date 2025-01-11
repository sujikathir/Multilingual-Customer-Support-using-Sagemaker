# File: multilingual-support/inference_handler.py

from typing import Dict, Optional, Tuple
from adapter_manager import LoraAdapterManager
from logger import setup_logger
import json

logger = setup_logger('inference_handler')

class CustomerSupportInference:
    def __init__(self):
        """Initialize the customer support inference handler"""
        self.adapter_manager = LoraAdapterManager()
        
    def _detect_language_and_domain(self, query: str) -> Tuple[str, str]:
        """
        Simple language and domain detection
        In a production system, you'd want to use a proper language detection model
        """
        # Simplified language detection based on common words
        language_markers = {
            'spanish': ['hola', 'gracias', 'por favor'],
            'french': ['bonjour', 'merci', 'sil vous plait'],
            'russian': ['привет', 'спасибо', 'пожалуйста']
        }
        
        # Simplified domain detection based on keywords
        domain_markers = {
            'technical': ['error', 'broken', 'not working', 'failed'],
            'billing': ['payment', 'charge', 'invoice', 'cost'],
            'product': ['features', 'specifications', 'compatibility']
        }
        
        # Detect language (defaulting to Spanish if uncertain)
        query_lower = query.lower()
        detected_language = 'spanish'
        detected_domain = 'technical'
        
        for lang, markers in language_markers.items():
            if any(marker in query_lower for marker in markers):
                detected_language = lang
                break
                
        for domain, markers in domain_markers.items():
            if any(marker in query_lower for marker in markers):
                detected_domain = domain
                break
                
        return detected_language, detected_domain

    def process_query(self, customer_query: str) -> Dict:
        """
        Process a customer query and return the response
        """
        try:
            # Detect language and domain
            language, domain = self._detect_language_and_domain(customer_query)
            logger.info(f"Detected language: {language}, domain: {domain}")
            
            # Get response using appropriate adapters
            response = self.adapter_manager.invoke_model(
                input_text=customer_query,
                language=language,
                domain=domain
            )
            
            return {
                'status': 'success',
                'language': language,
                'domain': domain,
                'query': customer_query,
                'response': response
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                'status': 'error',
                'error_message': str(e)
            }