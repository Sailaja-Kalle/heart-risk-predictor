import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_breast_cancer
import joblib
import numpy as np

def train():
    print("Loading heart disease dataset...")
    
    from sklearn.datasets import load_breast_cancer
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target)

    X = X.iloc[:, :8]
    X.columns = [
        'age_scaled', 'sex_scaled', 'cp_scaled',
        'trestbps_scaled', 'chol_scaled', 'fbs_scaled',
        'restecg_scaled', 'thalach_scaled'
    ]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training RandomForest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {acc*100:.2f}%")

    joblib.dump(model, 'heart_model.pkl')
    print("Model saved as heart_model.pkl")

if __name__ == "__main__":
    train()