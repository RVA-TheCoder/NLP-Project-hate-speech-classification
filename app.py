# from hate_speech.pipeline.train_pipeline import TrainPipeline
# obj=TrainPipeline()
# obj.run_pipeline()


from fastapi import FastAPI
import uvicorn
import sys
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response

from hate_speech.pipeline.train_pipeline import TrainPipeline
from hate_speech.pipeline.prediction_pipeline import PredictionPipeline

from hate_speech.exception import CustomException
from hate_speech.constants import *


#text:str = "What is machine learing?"

app = FastAPI()

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")



@app.post("/predict")
async def predict_route(text):
    
    try:

        obj = PredictionPipeline()
        result = obj.run_pipeline(text)
        
        return result
    
    except Exception as e:
        
        raise CustomException(e, sys) from e
    



if __name__=="__main__":
    
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
    
    # After running the app.py file from the powershell terminal
    # go to chrome and type the url for opening the app locally : http://localhost:8080/docs




