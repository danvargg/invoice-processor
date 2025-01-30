# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 80
EXPOSE 80

# Command to start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# TODO:
# docker build -t my-invoice-app .
#docker run -p 8000:80 --env-file .env my-invoice-app
#curl -X POST -F "files=@invoice1.pdf" -F "files=@invoice2.pdf" localhost:8000/invoices/

# Azure
# Azure Container Instances or Azure App Service
# Create Azure Container Registry (ACR) or push directly to Docker Hub.
#Build and push image to ACR/DockerHub:
#docker tag my-invoice-app <registry>.azurecr.io/my-invoice-app:latest
#docker push <registry>.azurecr.io/my-invoice-app:latest

# az container create \
#  --resource-group <your-resource-group> \
#  --name my-invoice-app \
#  --image <registry>.azurecr.io/my-invoice-app:latest \
#  --dns-name-label my-invoice-app-dns \
#  --ports 80 \
#  --environment-variables OPENAI_API_KEY="<YOUR-OPENAI-KEY>"

# AWS
# AWS ECS or AWS App Runner
# aws ecr create-repository --repository-name my-invoice-app
# docker tag my-invoice-app:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/my-invoice-app:latest
# docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/my-invoice-app:latest

# Deploy with ECS Fargate, AWS App Runner, or Elastic Beanstalk.
# Pass environment variables (OPENAI_API_KEY) in your ECS Task Definition or via the service's environment variable settings.