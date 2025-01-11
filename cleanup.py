# File: multilingual-support/cleanup.py

import boto3
import time
from logger import setup_logger
from config import SAGEMAKER_CONFIG, S3_CONFIG

logger = setup_logger('cleanup')

class ResourceCleaner:
    def __init__(self):
        """Initialize AWS clients"""
        self.sm_client = boto3.client('sagemaker')
        self.s3_client = boto3.client('s3')
        
    def delete_endpoint(self):
        """Delete SageMaker endpoint and associated resources"""
        try:
            # Delete endpoint
            logger.info(f"Attempting to delete endpoint: {SAGEMAKER_CONFIG['endpoint_name']}")
            try:
                self.sm_client.delete_endpoint(
                    EndpointName=SAGEMAKER_CONFIG['endpoint_name']
                )
                logger.info(f"Successfully deleted endpoint: {SAGEMAKER_CONFIG['endpoint_name']}")
            except self.sm_client.exceptions.ClientError as e:
                if 'Could not find endpoint' in str(e):
                    logger.info(f"Endpoint {SAGEMAKER_CONFIG['endpoint_name']} does not exist")
                else:
                    raise

            # Delete endpoint config
            logger.info(f"Attempting to delete endpoint config: {SAGEMAKER_CONFIG['endpoint_name']}-config")
            try:
                self.sm_client.delete_endpoint_config(
                    EndpointConfigName=f"{SAGEMAKER_CONFIG['endpoint_name']}-config"
                )
                logger.info(f"Successfully deleted endpoint config: {SAGEMAKER_CONFIG['endpoint_name']}-config")
            except self.sm_client.exceptions.ClientError as e:
                if 'Could not find endpoint configuration' in str(e):
                    logger.info(f"Endpoint config {SAGEMAKER_CONFIG['endpoint_name']}-config does not exist")
                else:
                    raise

            # Delete model
            logger.info(f"Attempting to delete model: {SAGEMAKER_CONFIG['endpoint_name']}")
            try:
                self.sm_client.delete_model(
                    ModelName=SAGEMAKER_CONFIG['endpoint_name']
                )
                logger.info(f"Successfully deleted model: {SAGEMAKER_CONFIG['endpoint_name']}")
            except self.sm_client.exceptions.ClientError as e:
                if 'Could not find model' in str(e):
                    logger.info(f"Model {SAGEMAKER_CONFIG['endpoint_name']} does not exist")
                else:
                    raise

        except Exception as e:
            logger.error(f"Error during endpoint cleanup: {str(e)}")
            raise

    def empty_and_delete_bucket(self, bucket_name):
        """Empty and delete an S3 bucket"""
        try:
            logger.info(f"Attempting to empty and delete bucket: {bucket_name}")
            
            # List and delete all objects in the bucket
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=bucket_name):
                if 'Contents' in page:
                    objects = [{'Key': obj['Key']} for obj in page['Contents']]
                    self.s3_client.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': objects}
                    )
                    logger.info(f"Deleted {len(objects)} objects from {bucket_name}")

            # Delete the bucket itself
            try:
                self.s3_client.delete_bucket(Bucket=bucket_name)
                logger.info(f"Successfully deleted bucket: {bucket_name}")
            except self.s3_client.exceptions.NoSuchBucket:
                logger.info(f"Bucket {bucket_name} does not exist")
                
        except Exception as e:
            logger.error(f"Error during bucket cleanup: {str(e)}")
            raise

    def cleanup_all(self):
        """Clean up all resources"""
        try:
            logger.info("Starting cleanup process...")
            
            # Delete SageMaker resources
            self.delete_endpoint()
            
            # Delete S3 buckets (only the LORA bucket, not the default SageMaker bucket)
            if S3_CONFIG.get('lora_bucket'):
                self.empty_and_delete_bucket(S3_CONFIG['lora_bucket'])
            
            logger.info("Cleanup completed successfully!")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            raise

def main():
    """Main function to run cleanup"""
    try:
        cleaner = ResourceCleaner()
        cleaner.cleanup_all()
    except Exception as e:
        logger.error(f"Main cleanup process failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()