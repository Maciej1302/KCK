from joblib import load
import sklearn
import pandas as pd
import xgboost


def load_pipeline():
    loaded_pipeline = load('credit_scoring_pipelinev0_3.joblib')
    return loaded_pipeline


def predict(user_data):
    credit_data = pd.DataFrame([user_data])
    pipeline = load_pipeline()
    pred = pipeline.predict_proba(credit_data)[:, 0]
    return round(pred[0], 0)

