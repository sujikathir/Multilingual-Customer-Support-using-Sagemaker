import boto3
import sagemaker
from logger import setup_logger
import logging

# Simple logger setup since we're in a notebook
logger = logging.getLogger('s3_setup')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

# S3 Configuration
S3_CONFIG = {
    'lora_bucket': 'multilingual-customer-support-lora',
    'adapter_prefix': 'lora-adapters/'
}

def setup_s3_resources():
    try:
        # Get the default SageMaker bucket
        session = sagemaker.Session()
        default_bucket = session.default_bucket()
        logger.info(f"Default SageMaker bucket: {default_bucket}")
        
        # Create S3 client
        s3 = boto3.client('s3')
        
        # Create LORA bucket if it doesn't exist
        try:
            s3.create_bucket(
                Bucket=S3_CONFIG['lora_bucket'],
                CreateBucketConfiguration={'LocationConstraint': session.boto_region_name}
            )
            logger.info(f"Created new bucket: {S3_CONFIG['lora_bucket']}")
        except s3.exceptions.BucketAlreadyExists:
            logger.info(f"Bucket already exists: {S3_CONFIG['lora_bucket']}")
        except s3.exceptions.BucketAlreadyOwnedByYou:
            logger.info(f"Bucket already owned by you: {S3_CONFIG['lora_bucket']}")
            
        # Create folder structure in LORA bucket
        folder_structure = [
            'lora-adapters/spanish/',
            'lora-adapters/french/',
            'lora-adapters/russian/',
            'lora-adapters/technical/',
            'lora-adapters/billing/',
            'lora-adapters/product/'
        ]
        
        for folder in folder_structure:
            s3.put_object(
                Bucket=S3_CONFIG['lora_bucket'],
                Key=folder
            )
            logger.info(f"Created folder: {folder}")
            
        return {
            'default_bucket': default_bucket,
            'lora_bucket': S3_CONFIG['lora_bucket']
        }
        
    except Exception as e:
        logger.error(f"Error setting up S3 resources: {str(e)}")
        raise

# Run the function
buckets = setup_s3_resources()
print("\nCreated buckets:", buckets)