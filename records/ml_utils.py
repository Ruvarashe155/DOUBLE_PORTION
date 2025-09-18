import joblib
import pandas as pd
import os

# Load the model and feature names once
model_path = os.path.join('ml_model', 'stock_predictor.pkl')
model, feature_names = joblib.load(model_path)  # <-- unpack tuple here

def predict_stock(user, product, unit_size, allocated, sold):
    data = {
        'unit_size': [unit_size],
        'allocated': [allocated],
        'sold': [sold],
        f'user_{user}': [1],
        f'product_{product}': [1],
    }

    # Fill missing one-hot columns with 0
    for col in feature_names:
        if col not in data:
            data[col] = [0]

    # Make sure columns are in the exact order as feature_names
    df = pd.DataFrame(data)[feature_names]

    predicted_remaining = model.predict(df)[0]
    return round(predicted_remaining, 2)
