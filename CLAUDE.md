# Heart Disease Risk Predictor

## Project Overview
Medical ML project that predicts heart disease risk 
from patient CSV data and generates PDF reports.

## Project Structure
- train_model.py → trains RandomForest model
- predictor.py → predicts risk from CSV
- report_agent.py → generates PDF report
- app.py → Gradio web UI

## How to run
1. python train_model.py
2. python app.py

## Rules
- Use scikit-learn for ML
- Use fpdf2 for PDF generation
- Use gradio for UI
- Save model as heart_model.pkl