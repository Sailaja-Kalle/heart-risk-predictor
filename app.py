import gradio as gr
import pandas as pd
from predictor import predict_risk
from report_agent import generate_report
import os

def analyze(csv_file):
    if csv_file is None:
        return None, None, "⚠️ Please upload a CSV file first!"
    
    try:
        predictions = predict_risk(csv_file.name)
        report_path = generate_report(predictions)
        df = pd.DataFrame(predictions)
        
        high = sum(1 for p in predictions if p['risk_level'] == 'HIGH')
        medium = sum(1 for p in predictions if p['risk_level'] == 'MEDIUM')
        low = sum(1 for p in predictions if p['risk_level'] == 'LOW')
        
        summary = f"""
### 📊 Analysis Complete!
| Risk Level | Count |
|------------|-------|
| 🔴 HIGH    | {high} patients |
| 🟡 MEDIUM  | {medium} patients |
| 🟢 LOW     | {low} patients |
| 👥 Total   | {len(predictions)} patients |
"""
        return df, report_path, summary
        
    except Exception as e:
        return None, None, f"❌ Error: {str(e)}"

css = """
* {
    font-family: 'Segoe UI', sans-serif;
}

body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.gradio-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    min-height: 100vh;
}

#header {
    background: linear-gradient(135deg, #c0392b, #e74c3c) !important;
    border-radius: 20px !important;
    padding: 30px !important;
    text-align: center !important;
    margin-bottom: 20px !important;
    box-shadow: 0 10px 30px rgba(192,57,43,0.4) !important;
}

#upload_section {
    background: white !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
    border: 2px dashed #e74c3c !important;
}

#analyze_btn {
    background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    font-weight: bold !important;
    padding: 15px !important;
    box-shadow: 0 6px 20px rgba(231,76,60,0.4) !important;
    transition: all 0.3s !important;
}

#analyze_btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(231,76,60,0.5) !important;
}

#summary_box {
    background: white !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
    border-left: 5px solid #e74c3c !important;
}

#results_section {
    background: white !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
}

#pdf_section {
    background: linear-gradient(135deg, #11998e, #38ef7d) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 4px 20px rgba(17,153,142,0.3) !important;
}

#footer {
    background: rgba(0,0,0,0.05) !important;
    border-radius: 12px !important;
    padding: 15px !important;
    text-align: center !important;
    margin-top: 20px !important;
}

.gr-dataframe {
    border-radius: 12px !important;
    overflow: hidden !important;
}
"""

with gr.Blocks(css=css, title="🫀 Heart Disease Risk Predictor") as app:

    with gr.Column(elem_id="header"):
        gr.HTML("""
        <div style='text-align:center'>
            <h1 style='color:white; font-size:2.5em; margin:0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3)'>
                🫀 Heart Disease Risk Predictor
            </h1>
            <p style='color:rgba(255,255,255,0.9); font-size:1.1em; margin-top:10px'>
                AI-Powered Medical Risk Analysis System
            </p>
            <div style='display:flex; justify-content:center; gap:20px; margin-top:15px'>
                <span style='background:rgba(255,255,255,0.2); padding:6px 14px; border-radius:20px; color:white; font-size:0.85em'>
                    ⚡ Instant Analysis
                </span>
                <span style='background:rgba(255,255,255,0.2); padding:6px 14px; border-radius:20px; color:white; font-size:0.85em'>
                    📄 PDF Report
                </span>
                <span style='background:rgba(255,255,255,0.2); padding:6px 14px; border-radius:20px; color:white; font-size:0.85em'>
                    🤖 ML Powered
                </span>
            </div>
        </div>
        """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML("""
            <div style='background:white; border-radius:16px; padding:20px; 
                        box-shadow:0 4px 20px rgba(0,0,0,0.1); margin-bottom:10px'>
                <h3 style='color:#c0392b; margin:0 0 10px 0'>📋 How to use</h3>
                <ol style='color:#555; line-height:1.8; margin:0; padding-left:20px'>
                    <li>Upload patient CSV file</li>
                    <li>Click Analyze button</li>
                    <li>View risk results</li>
                    <li>Download PDF report</li>
                </ol>
            </div>
            """)

            with gr.Column(elem_id="upload_section"):
                csv_input = gr.File(
                    label="📂 Upload Patient CSV File",
                    file_types=[".csv"]
                )
                analyze_btn = gr.Button(
                    "🔍 Analyze Patients",
                    variant="primary",
                    size="lg",
                    elem_id="analyze_btn"
                )

        with gr.Column(scale=2):
            with gr.Column(elem_id="summary_box"):
                summary_output = gr.Markdown(
                    value="### 👆 Upload a CSV file and click Analyze to see results"
                )

    with gr.Column(elem_id="results_section"):
        gr.HTML("<h3 style='color:#2c3e50; margin:0 0 15px 0'>📊 Patient Risk Results</h3>")
        results_table = gr.DataFrame(
            label="",
            wrap=True
        )

    with gr.Column(elem_id="pdf_section"):
        gr.HTML("""
        <h3 style='color:white; margin:0 0 10px 0'>
            📥 Download Full PDF Report
        </h3>
        <p style='color:rgba(255,255,255,0.8); margin:0 0 10px 0; font-size:0.9em'>
            Complete medical report with recommendations for all patients
        </p>
        """)
        pdf_output = gr.File(label="")

    with gr.Column(elem_id="footer"):
        gr.HTML("""
        <p style='color:#888; margin:0; font-size:0.85em'>
            ⚕️ This tool is for educational purposes only. 
            Always consult a qualified physician for medical decisions.
            Built with Python, Scikit-learn & Gradio
        </p>
        """)

    analyze_btn.click(
        fn=analyze,
        inputs=[csv_input],
        outputs=[results_table, pdf_output, summary_output]
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=True)