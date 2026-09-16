import os
from fpdf import FPDF

out_path = r"07_Final_Report\Q2_Final_Submission_Report.pdf"
md_path = r"07_Final_Report\Q2_Final_Report.md"

def clean(text):
    return text.replace('\u2014', '-').replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2192', '->')

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, 'Josh Talks AI: Transcriber Quality Evaluation', 0, 1, 'C')
        self.ln(2)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def h2(self, title):
        self.ln(4)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(41, 128, 185)
        self.cell(0, 8, clean(title.replace("## ", "")), 0, 1, 'L')
        self.ln(1)

    def h3(self, title):
        self.ln(2)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(52, 73, 94)
        self.cell(0, 6, clean(title.replace("### ", "")), 0, 1, 'L')
        self.ln(1)

    def body(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(30, 30, 30)
        clean_text = clean(text.replace('**', '').replace('`', '').replace('_', ''))
        self.multi_cell(0, 6, clean_text)
        self.ln(2)

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

with open(md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

buffer = []
def flush_buffer():
    if buffer:
        pdf.body(" ".join(buffer))
        buffer.clear()

for line in lines:
    line = line.strip()
    if not line or line == '---' or line.startswith('|'):
        flush_buffer()
        continue
    
    if line.startswith('# '):
        flush_buffer()
        continue
        
    if line.startswith('## '):
        flush_buffer()
        pdf.h2(line)
        
    elif line.startswith('### '):
        flush_buffer()
        pdf.h3(line)
        
    elif line.startswith('- '):
        flush_buffer()
        pdf.body(line)
        
    else:
        buffer.append(line)

flush_buffer()

pdf.output(out_path)
print(f"Professional PDF successfully generated at: {out_path}")
