# records/train_model.py

import os
import pandas as pd
from django.utils.timezone import make_aware
from records.models import user_stock_record
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

def train():
    # Load data from DB
    records = user_stock_record.objects.all().values()
    df = pd.DataFrame(records)

    if df.empty:
        print("No records found for training.")
        return

    # Convert date to datetime if not already
    df['date'] = pd.to_datetime(df['date'])

    # Use IDs instead of full names
    df = df.rename(columns={'user_id': 'user', 'product_id': 'product'})
    
    # One-hot encode
    df = pd.get_dummies(df, columns=['user', 'product'])

    # Prepare features and target
    X = df.drop(columns=['remaining', 'id', 'date','unit'], errors='ignore')
    y = df['remaining']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Save model and feature names
    os.makedirs('ml_model', exist_ok=True)
    joblib.dump((model, X_train.columns.tolist()), 'ml_model/stock_predictor.pkl')
    print("Model saved to ml_model/stock_predictor.pkl")
