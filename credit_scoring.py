from joblib import load
import sklearn
import pandas as pd


def load_pipeline():
    loaded_pipeline = load('credit_scoring_pipeline.joblib')
    return loaded_pipeline


def predict(user_data):
    credit_data = pd.DataFrame([user_data])
    pipeline = load_pipeline()
    pred = pipeline.predict(credit_data)[0]
    return pred

