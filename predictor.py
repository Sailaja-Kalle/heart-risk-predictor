import pandas as pd
import joblib
import numpy as np

def predict_risk(csv_file_path):
    print(f"Loading model...")
    model = joblib.load('heart_model.pkl')
    
    print(f"Reading CSV file...")
    df = pd.read_csv(csv_file_path)
    
    feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    X = df[feature_cols].iloc[:, :8]
    
    while X.shape[1] < 8:
        X[f'extra_{X.shape[1]}'] = 0
    
    X.columns = [
        'age_scaled', 'sex_scaled', 'cp_scaled',
        'trestbps_scaled', 'chol_scaled', 'fbs_scaled',
        'restecg_scaled', 'thalach_scaled'
    ]
    
    probabilities = model.predict_proba(X)[:, 1]
    predictions = []
    
    for i, (_, row) in enumerate(df.iterrows()):
        risk_score = round(float(probabilities[i]) * 100, 1)
        
        if risk_score >= 70:
            risk_level = "HIGH"
        elif risk_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        patient = {
            'patient_id': i + 1,
            'risk_score': risk_score,
            'risk_level': risk_level,
        }
        
        for col in df.columns[:5]:
            patient[col] = row[col]
        
        predictions.append(patient)
        print(f"Patient {i+1}: Risk {risk_score}% — {risk_level}")
    
    return predictions

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        results = predict_risk(sys.argv[1])
        print(f"\nTotal patients analyzed: {len(results)}")