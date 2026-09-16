import os
from fpdf import FPDF

# Local Path
pdf_path = 'JoshTalks_Project_Summary.pdf'

class PDF(FPDF):
    def header(self):
        # Title
        self.set_font('Arial', 'B', 16)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, 'Josh Talks AI: Transcriber Quality Evaluation', 0, 1, 'C')
        self.set_font('Arial', 'I', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'A Data-Driven Quality Control Framework for ASR Datasets', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        # Page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, body)
        self.ln(5)

# Create PDF
pdf = PDF()
pdf.add_page()

# Section 1
pdf.chapter_title("1. Project Overview & Purpose")
text1 = (
    "This project evaluates the quality of human transcribers using objective data signals rather than manual review. "
    "The goal is to automatically identify suspicious transcribers who rush tasks, barely review audio, or make minimal effort. "
    "This protects the integrity of AI training datasets (like Whisper AI)."
)
pdf.chapter_body(text1)

# Section 2
pdf.chapter_title("2. How the Workflow Operates (Kaise Kaam Karta Hai)")
text2 = (
    "The automated quality control system operates through a sequential data pipeline:\n\n"
    "1. Data Ingestion: The system expects the raw transcription_data.csv containing metrics like audio duration, time taken, and edit status.\n"
    "2. Feature Engineering: It calculates robust behavioral metrics:\n"
    "   - Time-to-Duration Ratio\n"
    "   - Edit Rates\n"
    "   - Median CPS (Character Per Second)\n"
    "3. Warning Sign Detection: Isolates anomalies, such as extreme low listening times or rapid copy-pasting of AI text without edits.\n"
    "4. Risk Scoring (Staged Action Plan):\n"
    "   - GREEN: Normal metrics (Allow work)\n"
    "   - YELLOW: Single weak signal (Monitor)\n"
    "   - ORANGE: Multiple warning signals (Restrict & Enhance QA)\n"
    "   - RED: Persistent severe anomalies (Block/Review)"
)
pdf.chapter_body(text2)

# Section 3
pdf.chapter_title("3. Technology Stack Used (Kya Tech Use Hua)")
text3 = (
    "- Language: Python 3.x\n"
    "- Data Processing: pandas, numpy (For fast vectorized feature engineering and outlier detection)\n"
    "- Data Output/Visualization: matplotlib (For plotting metric distributions), openpyxl (For Excel export)\n"
    "- Architecture: Modular script-based architecture (run_analysis.py) designed for robust pipeline integration."
)
pdf.chapter_body(text3)

# Section 4
pdf.chapter_title("4. Current Status & Dataset Availability")
text4 = (
    "This repository contains the complete analytical framework, formulas, and staging logic. Because the actual dataset was not provided, "
    "the project employs a 'Data-Unavailable Version' design. It features a fail-safe execution script (run_analysis.py) that detects the "
    "absence of data, preventing crashes while keeping the methodology perfectly primed for empirical calibration once the real data is supplied. "
    "No synthetic or fake data was fabricated, preserving complete professional integrity."
)
pdf.chapter_body(text4)

print("Generating Professional PDF using FPDF...")
pdf.output(pdf_path)
print(f"Success! PDF saved to: {pdf_path}")
