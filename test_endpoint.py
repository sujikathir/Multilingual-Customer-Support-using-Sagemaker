# File: multilingual-support/test_endpoint.py

import boto3
import json
from logger import setup_logger
from config import SAGEMAKER_CONFIG

logger = setup_logger('test_endpoint')

def test_endpoint():
    try:
        # Create a SageMaker runtime client
        runtime = boto3.client('sagemaker-runtime')
        
        # Test input
        payload = {
            "inputs": "Hello, how are you?",
            "parameters": {
                "max_new_tokens": 50,
                "temperature": 0.7
            }
        }
        
        # Invoke endpoint
        response = runtime.invoke_endpoint(
            EndpointName=SAGEMAKER_CONFIG['endpoint_name'],
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
        # Parse response
        result = json.loads(response['Body'].read().decode())
        logger.info(f"Model response: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error testing endpoint: {str(e)}")
        raise

if __name__ == "__main__":
    test_endpoint()