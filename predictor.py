from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

def train_model(data):
    data = data[['Close']].copy()
    data['Prediction'] = data['Close'].shift(-5)
    data.dropna(inplace=True)

    X = data[['Close']].values
    y = data['Prediction'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict_price(model, current_price):
    return model.predict(np.array([[current_price]]))[0]
