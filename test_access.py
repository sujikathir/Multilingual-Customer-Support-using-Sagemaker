# File: multilingual-support/test_access.py

import os
import boto3
from logger import setup_logger
from config import BASE_MODEL, SAGEMAKER_CONFIG

logger = setup_logger('test_access')


def test_huggingface_access():
    """Test HuggingFace model access"""
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        
        # Get token from SAGEMAKER_CONFIG
        hf_token = SAGEMAKER_CONFIG['environment']['HUGGING_FACE_HUB_TOKEN']
        
        # Check token
        if not hf_token:
            logger.error("HUGGING_FACE_HUB_TOKEN not set in config.py")
            return False
            
        # Set the token for huggingface-hub
        os.environ['HUGGING_FACE_HUB_TOKEN'] = hf_token
            
        # Test model access
        model_info = api.model_info(BASE_MODEL['model_id'])
        logger.info(f"Successfully accessed model: {model_info.modelId}")
        return True
    except Exception as e:
        logger.error(f"HuggingFace access test failed: {str(e)}")
        return False

def test_sagemaker_access():
    """Test SageMaker access"""
    try:
        client = boto3.client('sagemaker')
        client.list_endpoints(MaxResults=1)
        logger.info("Successfully accessed SageMaker")
        return True
    except Exception as e:
        logger.error(f"SageMaker access test failed: {str(e)}")
        return False

def run_tests():
    """Run all access tests"""
    hf_access = test_huggingface_access()
    sm_access = test_sagemaker_access()
    
    if hf_access and sm_access:
        logger.info("All access tests passed!")
        return True
    return False

if __name__ == "__main__":
    run_tests()