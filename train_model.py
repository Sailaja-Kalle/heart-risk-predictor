import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def train():
    np.random.seed(42)
    n = 500

    # HIGH RISK patients
    high = pd.DataFrame({
        'age_scaled': np.random.randint(55, 75, 170),
        'sex_scaled': np.random.randint(0, 2, 170),
        'cp_scaled': np.random.randint(3, 5, 170),
        'trestbps_scaled': np.random.randint(140, 180, 170),
        'chol_scaled': np.random.randint(250, 420, 170),
        'fbs_scaled': np.ones(170),
        'restecg_scaled': np.random.randint(1, 3, 170),
        'thalach_scaled': np.random.randint(90, 130, 170),
        'target': np.ones(170)
    })

    # MEDIUM RISK patients
    medium = pd.DataFrame({
        'age_scaled': np.random.randint(45, 60, 160),
        'sex_scaled': np.random.randint(0, 2, 160),
        'cp_scaled': np.random.randint(2, 4, 160),
        'trestbps_scaled': np.random.randint(120, 145, 160),
        'chol_scaled': np.random.randint(200, 260, 160),
        'fbs_scaled': np.random.randint(0, 2, 160),
        'restecg_scaled': np.ones(160),
        'thalach_scaled': np.random.randint(130, 160, 160),
        'target': np.ones(160) * 0.5
    })

    # LOW RISK patients
    low = pd.DataFrame({
        'age_scaled': np.random.randint(25, 50, 170),
        'sex_scaled': np.random.randint(0, 2, 170),
        'cp_scaled': np.ones(170),
        'trestbps_scaled': np.random.randint(90, 125, 170),
        'chol_scaled': np.random.randint(150, 210, 170),
        'fbs_scaled': np.zeros(170),
        'restecg_scaled': np.zeros(170),
        'thalach_scaled': np.random.randint(155, 190, 170),
        'target': np.zeros(170)
    })

    df = pd.concat([high, medium, low], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Make medium target binary for training
    df['target'] = df['target'].apply(lambda x: 1 if x >= 0.5 else 0)

    X = df.drop('target', axis=1)
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Model Accuracy: {acc*100:.2f}%")

    joblib.dump(model, 'heart_model.pkl')
    print("Model saved!")

if __name__ == "__main__":
    train()