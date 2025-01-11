# File: multilingual-support/adapter_manager.py

import boto3
import json
import os
from typing import Dict, Optional
from logger import setup_logger
from config import ADAPTER_CONFIGS, SAGEMAKER_CONFIG

logger = setup_logger('adapter_manager')

class LoraAdapterManager:
    def __init__(self, endpoint_name: str = SAGEMAKER_CONFIG['endpoint_name']):
        """Initialize the LORA adapter manager"""
        self.runtime = boto3.client('sagemaker-runtime')
        self.endpoint_name = endpoint_name
        self.current_language = None
        self.current_domain = None

    def _format_prompt(self, input_text: str, language: str, domain: str) -> Dict:
        """Format the input prompt with adapter information"""
        adapter_name = f"{ADAPTER_CONFIGS['languages'][language]['name']}-{ADAPTER_CONFIGS['domains'][domain]}"
        
        return {
            "inputs": input_text,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
                "do_sample": True,
                "adapter_name": adapter_name
            }
        }

    def invoke_model(self, input_text: str, language: str = 'spanish', domain: str = 'technical') -> str:
        """
        Invoke the model with specified language and domain adapters
        """
        try:
            # Format the prompt with adapter information
            payload = self._format_prompt(input_text, language, domain)
            
            # Add retry logic
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    response = self.runtime.invoke_endpoint(
                        EndpointName=self.endpoint_name,
                        ContentType='application/json',
                        Body=json.dumps(payload)
                    )
                    result = json.loads(response['Body'].read().decode())
                    return result['generated_text']
                
                except self.runtime.exceptions.ModelError:
                    logger.warning(f"Model error occurred. Retry {retry_count + 1}/{max_retries}")
                    retry_count += 1
                    if retry_count == max_retries:
                        raise
                    time.sleep(1)  # Wait before retrying
                
                except Exception as e:
                    logger.error(f"Error invoking model: {str(e)}")
                    raise
    
        except Exception as e:
            logger.error(f"Error invoking model: {str(e)}")
            raise