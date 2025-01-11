# File: multilingual-support/sagemaker_setup.py

import boto3
import sagemaker
from sagemaker import get_execution_role
import logging
from logger import setup_logger
from config import AWS_CONFIG, BASE_MODEL, SAGEMAKER_CONFIG, ADAPTER_CONFIGS

# Initialize logger
logger = setup_logger('sagemaker_setup')

class MultilingualSupportDeployment:
    def __init__(self):
        """Initialize SageMaker deployment resources"""
        try:
            self.session = sagemaker.Session()
            self.account_id = boto3.client('sts').get_caller_identity()['Account']
            self.sm_client = boto3.client('sagemaker', region_name=AWS_CONFIG['region'])
            self.runtime = boto3.client('sagemaker-runtime', region_name=AWS_CONFIG['region'])
            self.role = AWS_CONFIG['role_arn'] or get_execution_role()
            logger.info("Successfully initialized SageMaker resources")
        except Exception as e:
            logger.error(f"Failed to initialize SageMaker resources: {str(e)}")
            raise

    def get_container_uri(self):
        """Get the LMI container URI for model deployment"""
        try:
            container_uri = sagemaker.image_uris.retrieve(
                framework='djl-deepspeed',
                region=AWS_CONFIG['region'],
                version=SAGEMAKER_CONFIG['container_version']
            )
            logger.info(f"Retrieved container URI: {container_uri}")
            return container_uri
        except Exception as e:
            logger.error(f"Failed to get container URI: {str(e)}")
            raise

    def create_model(self):
        """Create the SageMaker model with LORA configuration"""
        try:
            container_uri = self.get_container_uri()
            
            # Environment variables for LORA configuration
            environment = {
                'HF_MODEL_ID': BASE_MODEL['model_id'],
                'OPTION_ENABLE_LORA': 'true',
                'MAX_LORA_RANK': str(SAGEMAKER_CONFIG['max_lora_rank']),
                'MAX_CPU_LORA': str(SAGEMAKER_CONFIG['max_cpu_lora']),
                **SAGEMAKER_CONFIG['environment']
            }

            # Create model
            response = self.sm_client.create_model(
                ModelName=SAGEMAKER_CONFIG['endpoint_name'],
                ExecutionRoleArn=self.role,
                Containers=[{
                    'Image': container_uri,
                    'Environment': environment,
                }]
            )
            logger.info(f"Successfully created model: {SAGEMAKER_CONFIG['endpoint_name']}")
            return response
        except Exception as e:
            logger.error(f"Failed to create model: {str(e)}")
            raise

    def create_endpoint_config(self):
        """Create the endpoint configuration"""
        try:
            response = self.sm_client.create_endpoint_config(
                EndpointConfigName=f"{SAGEMAKER_CONFIG['endpoint_name']}-config",
                ProductionVariants=[{
                    'InstanceType': BASE_MODEL['instance_type'],
                    'InitialInstanceCount': 1,
                    'ModelName': SAGEMAKER_CONFIG['endpoint_name'],
                    'VariantName': 'AllTraffic',
                    'ContainerStartupHealthCheckTimeoutInSeconds': 600,
                    'ModelDataDownloadTimeoutInSeconds': 900,
                }]
            )
            logger.info(f"Successfully created endpoint config: {SAGEMAKER_CONFIG['endpoint_name']}-config")
            return response
        except Exception as e:
            logger.error(f"Failed to create endpoint config: {str(e)}")
            raise

    def create_endpoint(self):
        """Create and deploy the endpoint"""
        try:
            response = self.sm_client.create_endpoint(
                EndpointName=SAGEMAKER_CONFIG['endpoint_name'],
                EndpointConfigName=f"{SAGEMAKER_CONFIG['endpoint_name']}-config"
            )
            
            logger.info(f"Creating endpoint: {SAGEMAKER_CONFIG['endpoint_name']}")
            
            # Wait for endpoint to be ready
            waiter = self.sm_client.get_waiter('endpoint_in_service')
            waiter.wait(
                EndpointName=SAGEMAKER_CONFIG['endpoint_name'],
                WaiterConfig={'Delay': 30, 'MaxAttempts': 60}
            )
            
            logger.info(f"Successfully created endpoint: {SAGEMAKER_CONFIG['endpoint_name']}")
            return response
        except Exception as e:
            logger.error(f"Failed to create endpoint: {str(e)}")
            raise

    def deploy(self):
        """Deploy the complete multilingual support system"""
        try:
            logger.info("Starting deployment process...")
            self.create_model()
            self.create_endpoint_config()
            self.create_endpoint()
            logger.info("Deployment completed successfully!")
        except Exception as e:
            logger.error(f"Deployment failed: {str(e)}")
            self.cleanup()
            raise

    def verify_setup(self):
        """Verify AWS setup and permissions"""
        try:
            # Test S3 access
            s3 = boto3.client('s3')
            s3.head_bucket(Bucket=S3_CONFIG['bucket'])
            
            # Test IAM role
            iam = boto3.client('iam')
            role_name = self.role.split('/')[-1]
            iam.get_role(RoleName=role_name)
            
            # Test SageMaker access
            self.sm_client.list_endpoints(MaxResults=1)
            
            logger.info("Successfully verified AWS setup and permissions")
            return True
        except Exception as e:
            logger.error(f"Setup verification failed: {str(e)}")
            return False

    def cleanup(self):
        """Clean up resources in case of failure"""
        try:
            # Delete endpoint
            try:
                self.sm_client.delete_endpoint(EndpointName=SAGEMAKER_CONFIG['endpoint_name'])
                logger.info(f"Deleted endpoint: {SAGEMAKER_CONFIG['endpoint_name']}")
            except:
                pass

            # Delete endpoint config
            try:
                self.sm_client.delete_endpoint_config(
                    EndpointConfigName=f"{SAGEMAKER_CONFIG['endpoint_name']}-config"
                )
                logger.info(f"Deleted endpoint config: {SAGEMAKER_CONFIG['endpoint_name']}-config")
            except:
                pass

            # Delete model
            try:
                self.sm_client.delete_model(ModelName=SAGEMAKER_CONFIG['endpoint_name'])
                logger.info(f"Deleted model: {SAGEMAKER_CONFIG['endpoint_name']}")
            except:
                pass

        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    deployment = MultilingualSupportDeployment()
    deployment.deploy()

    # Verify setup before proceeding
    if deployment.verify_setup():
        deployment.deploy()
    else:
        logger.error("Setup verification failed. Please check your AWS configurations")
        exit(1)