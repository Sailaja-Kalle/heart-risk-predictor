import joblib
import pandas as pd
import numpy as np

model = joblib.load('heart_model.pkl')

def predict_risk(df):
    required_cols = ['age_scaled', 'sex_scaled', 'cp_scaled', 'trestbps_scaled', 
                     'chol_scaled', 'fbs_scaled', 'restecg_scaled', 'thalach_scaled']
    X = df[required_cols]
    probas = model.predict_proba(X)[:, 1]
    
    # Use percentile-based thresholds so all 3 levels always appear
    high_thresh = np.percentile(probas, 67)   # top 33% = HIGH
    low_thresh = np.percentile(probas, 33)    # bottom 33% = LOW
    
    risk_scores = []
    risk_levels = []
    for p in probas:
        score = int(p * 100)
        if p >= high_thresh:
            level = 'HIGH'
        elif p <= low_thresh:
            level = 'LOW'
        else:
            level = 'MEDIUM'
        risk_scores.append(score)
        risk_levels.append(level)
    
    result = df.copy()
    result.insert(0, 'patient_id', range(1, len(df)+1))
    result.insert(1, 'risk_score', risk_scores)
    result.insert(2, 'risk_level', risk_levels)
    return result