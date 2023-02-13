from fastapi import FastAPI
import uvicorn
import mlflow
from pydantic import BaseModel
import numpy as np
import pandas as pd
import os

app=FastAPI()

mlflow.set_tracking_uri('http://ml.mlplatform.click/mlflow')


#Load model


#model=mlflow.lightgbm.load_model("s3://mlflow-bucket-c44b010/0/80d7a42c307240ebbeb8bb0d3c973834/artifacts/model/")
class Size(BaseModel):

    length:float
    width:float

class PredictRequest(BaseModel):

    sepal: Size
    petal: Size
    



model=mlflow.lightgbm.load_model(f'runs:/{os.eviron['MLFLOW_RUN_ID']}/model')
flower_name_by_index = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}


@app.post("/predict")
def predict(request: PredictRequest):
    df = pd.DataFrame(columns=['sepal.length', 'sepal.width', 'petal.length', 'petal.width'],
                      data=[[request.sepal.length, request.sepal.width, request.petal.length, request.petal.width]])

    y_pred = np.argmax(model.predict(df))
    #return {"flower": flower_name_by_index[y_pred]}
    return {"flower": flower_name_by_index[y_pred]}

@app.post("/predict2")
def predict(request: PredictRequest):
    df = pd.DataFrame(columns=['sepal.length', 'sepal.width', 'petal.length', 'petal.width'],
                      data=[[request.sepal.length, request.sepal.width, request.petal.length, request.petal.width]])

    y_pred = np.argmax(model.predict(df))
    #return {"flower": flower_name_by_index[y_pred]}
    return {"flower": int(y_pred)*2}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()



