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


## Deployment

1. Setting up circleCI
2. Switch on self hosted runner on CircleCi
3. Create Project ON CircleCi
4. Configure EC2 on AWS
5. config.yml file inside .circleci folder
6. env variables (set inside CircleCi project settings)

