# Multilingual AI Customer Support System using AWS SageMaker and LORA

A scalable multilingual customer support system that demonstrates how to efficiently deploy and manage multiple language models using AWS SageMaker and LORA adapters. This system can handle customer queries in Spanish, French, and Russian while maintaining specialized support across technical, billing, and product domains.

## Features
- Cost-efficient multilingual support using LORA adapters
- Dynamic adapter loading for optimal resource utilization  
- Concurrent request handling with batching
- Language and domain detection
- Comprehensive logging and monitoring
- Automated cleanup and resource management

## Architecture
The system uses:
- Base Model: Hosted on SageMaker using LMI container
- LORA Adapters: Language and domain-specific adapters
- G5 Instance: NVIDIA A10G GPU for efficient inference
- S3 Storage: For adapter management

## Prerequisites
- AWS Account with SageMaker access
- Python 3.8+

## 1. Installation
1. Clone the repository:
```bash
git clone https://github.com/sujikathir/Multilingual-Customer-Support-using-Sagemaker.git
```

## 2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 3. Configuration

Update config.py with your settings:

AWS region
Instance type
Model configurations
Adapter settings

## 4. Deployment

- Initialize SageMaker resources:

```bash
python sagemaker_setup.py
```
- Verify the setup:

```bash
python test_access.py
```

- Test the endpoint:

```bash
python test_endpoint.py
```

## 5. Usage

Example of processing a customer query:
```bash
from inference_handler import CustomerSupportInference

handler = CustomerSupportInference()
response = handler.process_query("Hola, necesito ayuda técnica")
print(response)
```

## 6. Resource Management
Clean up resources when done:
```bash
python cleanup.py
```

## 7. Cost Optimization

- Uses unmerged LORA inference to minimize GPU memory usage
- Dynamic adapter loading reduces resource requirements
- Batching for efficient request processing
- Automatic resource cleanup

## 8. Performance

Response time: ~2-3 seconds per query
Concurrent requests: Up to 4 per GPU
Memory usage: ~24GB GPU memory
Cost: ~70% lower than traditional deployment


