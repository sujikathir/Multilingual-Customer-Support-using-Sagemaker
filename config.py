# File: multilingual-support/config/config.py

import os
from typing import Dict, Any

# AWS Configuration
AWS_CONFIG = {
    'region': os.getenv('AWS_REGION', 'us-east-2'),
    'role_arn': os.getenv('AWS_ROLE_ARN', 'arn:aws:iam::387311887840:role/service-role/AmazonSageMaker-ExecutionRole-20241216T145914'),  # You'll need to set this
}

# Base Model Configuration
BASE_MODEL = {
    'model_id': 'HuggingFaceH4/zephyr-7b-beta',  # We'll use 7B for demonstration
    'instance_type': 'ml.g5.2xlarge',  # Can be adjusted based on needs
}

# LORA Adapter Configurations
ADAPTER_CONFIGS = {
    'languages': {
        'spanish': {
            'name': 'es',
            'adapter_id': 'spanish-customer-support'
        },
        'french': {
            'name': 'fr',
            'adapter_id': 'french-customer-support'
        },
        'russian': {
            'name': 'ru',
            'adapter_id': 'russian-customer-support'
        }
    },
    'domains': {
        'technical': 'technical-support',
        'billing': 'billing-support',
        'product': 'product-support'
    }
}

# SageMaker Deployment Configuration

SAGEMAKER_CONFIG = {
    'endpoint_name': 'multilingual-support',
    'container_version': '0.27.0',
    'max_concurrent_transforms': 4,
    'enable_unmerged_lora': True,
    'max_lora_rank': 64,  # From video recommendation
    'max_cpu_lora': 4,    # Number of LORA adapters to cache in CPU
    'environment': {
        'TENSOR_PARALLEL_DEGREE': 'max',
        'ROLLING_BATCH': 'auto',
        'MAX_ROLLING_BATCH_SIZE': '32',
        'MAX_INPUT_LENGTH': '2048',
        'MAX_TOTAL_TOKENS': '4096',
        'HUGGING_FACE_HUB_TOKEN': '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', # Your Hugging Face Access token
        'DTYPE': 'fp16'
    }
}

# Update the S3_CONFIG section:
S3_CONFIG = {
    'default_bucket': None,  # Will be populated with SageMaker default bucket
    'lora_bucket': 'multilingual-customer-support-lora',  # We'll create this
    'adapter_prefix': 'lora-adapters/'
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_path': 'logs/application.log'
}