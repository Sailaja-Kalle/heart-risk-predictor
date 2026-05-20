from fpdf import FPDF
from datetime import datetime

def generate_report(predictions, output_path="heart_report.pdf"):
    print("Generating PDF report...")
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_fill_color(220, 50, 50)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_xy(0, 8)
    pdf.cell(210, 10, "HEART DISEASE RISK REPORT", align="C", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(210, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C", ln=True)
    pdf.cell(210, 8, f"Total Patients Analyzed: {len(predictions)}", align="C", ln=True)
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    
    high = sum(1 for p in predictions if p['risk_level'] == 'HIGH')
    medium = sum(1 for p in predictions if p['risk_level'] == 'MEDIUM')
    low = sum(1 for p in predictions if p['risk_level'] == 'LOW')
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, "SUMMARY", ln=True, fill=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 7, f"  HIGH Risk Patients   : {high}", ln=True)
    pdf.set_text_color(200, 140, 0)
    pdf.cell(0, 7, f"  MEDIUM Risk Patients : {medium}", ln=True)
    pdf.set_text_color(0, 150, 0)
    pdf.cell(0, 7, f"  LOW Risk Patients    : {low}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    for p in predictions:
        pdf.set_font("Helvetica", "B", 12)
        
        if p['risk_level'] == 'HIGH':
            pdf.set_fill_color(255, 220, 220)
        elif p['risk_level'] == 'MEDIUM':
            pdf.set_fill_color(255, 245, 200)
        else:
            pdf.set_fill_color(220, 255, 220)
        
        pdf.cell(0, 8, 
            f"Patient {p['patient_id']}  |  Risk Score: {p['risk_score']}%  |  Level: {p['risk_level']}",
            ln=True, fill=True
        )
        
        pdf.set_font("Helvetica", "", 10)
        
        keys = [k for k in p.keys() if k not in ['patient_id', 'risk_score', 'risk_level']]
        for key in keys:
            pdf.cell(0, 6, f"    {key}: {p[key]}", ln=True)
        
        pdf.set_font("Helvetica", "I", 10)
        if p['risk_level'] == 'HIGH':
            pdf.set_text_color(200, 0, 0)
            pdf.cell(0, 6, "    Recommendation: Immediate cardiology referral advised", ln=True)
        elif p['risk_level'] == 'MEDIUM':
            pdf.set_text_color(180, 100, 0)
            pdf.cell(0, 6, "    Recommendation: Schedule follow-up within 30 days", ln=True)
        else:
            pdf.set_text_color(0, 130, 0)
            pdf.cell(0, 6, "    Recommendation: Routine annual checkup sufficient", ln=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)
    
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 6, "This report is AI-assisted. Final diagnosis must be made by a qualified physician.", ln=True)
    
    pdf.output(output_path)
    print(f"PDF report saved as {output_path}")
    return output_path