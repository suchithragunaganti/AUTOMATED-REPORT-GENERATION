
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt  # For creating charts

# Read CSV data
data = pd.read_csv("data.csv")

# Analyze the data
average_score = data['Score'].mean()
top_score = data['Score'].max()
department_group = data.groupby('Department')['Score'].mean()

# Generate and save chart
plt.figure(figsize=(5, 4))
department_group.plot(kind='bar', color='skyblue')
plt.title('Average Score by Department')
plt.ylabel('Score')
plt.tight_layout()
plt.savefig('chart.png')
plt.close()

# Create PDF report
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Automated Report', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_table(self, data):
        self.set_font("Arial", 'B', 12)
        self.cell(60, 10, 'Name', 1)
        self.cell(60, 10, 'Department', 1)
        self.cell(40, 10, 'Score', 1)
        self.ln()

        self.set_font("Arial", '', 12)
        for _, row in data.iterrows():
            self.cell(60, 10, str(row['Name']), 1)
            self.cell(60, 10, str(row['Department']), 1)
            self.cell(40, 10, str(row['Score']), 1)
            self.ln()
        self.ln(10)

    def add_chart(self, path):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Department Average Score Chart:', ln=True)
        self.image(path, w=180)
        self.ln(10)

    def add_summary(self, avg, top, dept_group):
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, "Summary:", ln=True)
        self.set_font("Arial", '', 12)
        self.cell(0, 10, f"Average Score: {avg:.2f}", ln=True)
        self.cell(0, 10, f"Top Score: {top}", ln=True)
        self.ln(5)
        self.cell(0, 10, "Average by Department:", ln=True)
        for dept, score in dept_group.items():
            self.cell(0, 10, f" - {dept}: {score:.2f}", ln=True)

# Generate the PDF
pdf = PDF()
pdf.add_page()
pdf.add_table(data)
pdf.add_chart('chart.png')  # Chart inserted here
pdf.add_summary(average_score, top_score, department_group)
pdf.output("report.pdf")
print("✅ PDF report generated as 'report.pdf'")
