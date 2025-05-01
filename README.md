# End-to-end-NLP-Project-Implementation


## Project Workflows

- hate_speech/constants/__init__.py file  
- hate_speech/entity/config_entity.py file
- hate_speech/entity/artifact_entity.py file     
- components
- pipeline
- app.py


## How to run?

```bash
conda create -n hate python=3.8 -y
```

```bash
conda activate hate
```

```bash
pip install -r requirements.txt
```

```bash
python app.py
```


# Gcloud cli
https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe

```bash
before running this command in powershell run below command at poweshell cli :  
syntax : Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Above command will Temporarily Bypass Execution Policy (Recommended)
If you don’t want to change system settings permanently, just bypass the policy for the current session:
then run


gcloud init
```


# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

## 2. Create IAM user for deployment

	#with specific access

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	
## 3. Create ECR repo to store/save docker image
    - Save the ECR URI: for eg., 56637...765.dkr.ecr.us-east-1.amazonaws.com/chicken

	
## 4. Create EC2 machine (Ubuntu) 

## 5. Open EC2 and Install docker in EC2 Machine by running below commands at the EC2 terminal:
	
	#optional

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
# 6. Configure EC2 as self-hosted runner:
    - inside github project repo goto :->  setting>actions>runner>new self hosted runner> choose os> 
	- then run commands one by one at the EC2 terminal mentioned by github while creating the `self-hosted` runner.

# 7. Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to AWS ECR

	3. Launch Your AWS EC2 instance

	4. Pull Your image from ECR into EC2

	5. Lauch your docker image in EC2 instance

# 8. Setup github secrets:

    AWS_ACCESS_KEY_ID=<from iam user .csv file>

    AWS_SECRET_ACCESS_KEY=<from iam user .csv file>

    AWS_REGION = ap-south-1

    AWS_ECR_LOGIN_URI = <your ecr uri>

    ECR_REPOSITORY_NAME = <your-ecr-name>

