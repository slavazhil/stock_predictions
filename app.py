import yfinance as yf
from sklearn.multioutput import RegressorChain
from sklearn.svm import LinearSVR
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

LOOK_BACK = 50
PREDICT_FORWARD = 5

def handler(event, context):
    print(event)
    try:
        ticker = event["queryStringParameters"]["ticker"]
        interval = event["queryStringParameters"]["interval"]
        predictions = predict(ticker, interval)
        print("RESULT:", ticker, interval, predictions)
        return predictions
    except Exception as e:
        print("ERROR:", e)
        return {"error": "Bad Request"}

def predict(ticker, interval):
    period = "max" if interval == "d" else "1y"
    interval = "1" + interval
    df = pd.DataFrame(yf.Ticker(ticker).history(interval=interval, period=period))
    #Reshape the data
    data = df["Close"].values
    X = []
    y = []

    for i in range(0,len(data)-LOOK_BACK-PREDICT_FORWARD):
        X.append(data[i:i+LOOK_BACK])
        y.append(data[i+LOOK_BACK:i+LOOK_BACK+PREDICT_FORWARD])

    # define base model
    model = LinearSVR(dual=False, loss="squared_epsilon_insensitive")
    # define the chained multioutput wrapper model
    wrapper = RegressorChain(model)
    # fit the model on the whole dataset
    wrapper.fit(X, y)
    # make prediction
    historic_data = data[len(data)-LOOK_BACK:]
    prediction = wrapper.predict([historic_data])[0]
    return prediction.tolist()
