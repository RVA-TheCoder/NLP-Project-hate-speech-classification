# End-to-end-NLP-Project-Implementation


## Project Workflows

- constants
- config_enity
- artifact_enity
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
2. Switch on self hosted runner
3. Create Project
4. Configure EC2
5. config.yml
6. env variables

