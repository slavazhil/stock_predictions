import yfinance as yf
from sklearn.multioutput import RegressorChain
from sklearn.svm import LinearSVR
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

LOOK_BACK = 50
PREDICT_FORWARD = 50

FIVE_DAYS = 1000 * 60 * 60 * 24 * 5
ONE_DAY = 1000 * 60 * 60 * 24
THIRTY_MINUTES = 1000 * 60 * 30
FIVE_MINUTES = 1000 * 60 * 5

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
    period = "max" if interval in ["1d", "5d"] else "1mo"
    df = pd.DataFrame(yf.Ticker(ticker).history(interval=interval, period=period))
    df.dropna(inplace=True)
    last_timestamp = int(df.index[-1].timestamp()*1000)
    print("LAST_TIMESTAMP:", last_timestamp)
    #Reshape the data
    data = df["Close"].values
    X = []
    y = []

    for i in range(0,len(data)-LOOK_BACK-PREDICT_FORWARD):
        X.append(data[i:i+LOOK_BACK])
        y.append(data[i+LOOK_BACK:i+LOOK_BACK+PREDICT_FORWARD])

    print("X_LENGTH:", len(X))
    print("y_LENGTH:", len(y))

    # define base model
    model = LinearSVR(dual=False, loss="squared_epsilon_insensitive")
    # define the chained multioutput wrapper model
    wrapper = RegressorChain(model)
    # fit the model on the whole dataset
    wrapper.fit(X, y)
    # make prediction
    historic_data = data[len(data)-LOOK_BACK:]
    predictions = wrapper.predict([historic_data])[0].tolist()

    payload = []
    time_increment = 0

    if interval == "5m":
        time_increment = FIVE_MINUTES
    elif interval == "30m":
        time_increment = THIRTY_MINUTES
    elif interval == "1d":
        time_increment = ONE_DAY
    elif interval == "5d":
        time_increment = FIVE_DAYS

    print("TIME_INCREMENT:", time_increment)

    for p in predictions:
        last_timestamp += time_increment
        payload.append({"date": last_timestamp, "price": p})

    return {"response_code": 200, "payload": payload}
