# File: multilingual-support/test_inference.py

from inference_handler import CustomerSupportInference
from logger import setup_logger

logger = setup_logger('test_inference')

def test_customer_support():
    handler = CustomerSupportInference()
    
    # Test queries in different languages and domains
    test_queries = [
        # Spanish queries
        "Hola, mi producto no está funcionando correctamente",  # Technical
        "Necesito información sobre mi última factura",        # Billing
        
        # French queries
        "Bonjour, je ne peux pas accéder à mon compte",       # Technical
        "Quelles sont les caractéristiques du produit?",      # Product
        
        # Russian queries
        "Привет, мой продукт сломался",                       # Technical
        "Сколько стоит подписка?",                           # Billing
    ]
    
    for query in test_queries:
        logger.info(f"\nProcessing query: {query}")
        result = handler.process_query(query)
        logger.info(f"Result: {result}")

if __name__ == "__main__":
    test_customer_support()