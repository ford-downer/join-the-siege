from fpdf import FPDF
import os
from docx import Document

def create_pdf(content, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for line in content.split('\n'):
        pdf.cell(200, 10, txt=line.strip(), ln=True, align='L')
    
    pdf.output(output_file)

def create_docx(content, output_file):
    doc = Document()
    for line in content.split('\n'):
        doc.add_paragraph(line)
    doc.save(output_file)

# Ensure files directory exists
os.makedirs("files", exist_ok=True)

# Sample documents
invoices = [
    {
        "number": "INV-2024-001",
        "amount": 1500,
        "items": ["Web Development", "UI Design"],
        "client": "Tech Corp"
    },
    {
        "number": "INV-2024-002",
        "amount": 2500,
        "items": ["Mobile App Development", "Testing"],
        "client": "Digital Solutions"
    },
    {
        "number": "INV-2024-003",
        "amount": 3000,
        "items": ["Cloud Migration", "Training"],
        "client": "Cloud Systems Inc"
    }
]

bank_statements = [
    {
        "bank": "Pacific Bank",
        "account": "****1234",
        "balance": 5000,
        "transactions": ["Salary Credit: $3000", "Rent Payment: -$1500"]
    },
    {
        "bank": "Atlantic Bank",
        "account": "****5678",
        "balance": 7500,
        "transactions": ["Investment Return: $500", "Utility Bill: -$200"]
    },
    {
        "bank": "Mountain Bank",
        "account": "****9012",
        "balance": 10000,
        "transactions": ["Business Income: $5000", "Office Supplies: -$300"]
    }
]

licenses = [
    {
        "name": "John Smith",
        "dob": "1990-05-15",
        "state": "California",
        "number": "CA12345678"
    },
    {
        "name": "Emma Johnson",
        "dob": "1985-08-22",
        "state": "New York",
        "number": "NY87654321"
    },
    {
        "name": "Michael Brown",
        "dob": "1978-11-30",
        "state": "Texas",
        "number": "TX11223344"
    }
]

# Create invoice PDFs and Word docs
for i, inv in enumerate(invoices, 1):
    content = f"""INVOICE

Invoice Number: {inv['number']}
Client: {inv['client']}

Items:
{chr(10).join(f"- {item}" for item in inv['items'])}

Total Amount: ${inv['amount']}

Payment Terms: Net 30
Thank you for your business!"""
    
    create_pdf(content, f"files/invoice_{i}.pdf")
    create_docx(content, f"files/invoice_{i}.docx")

# Create bank statement PDFs and Word docs
for i, stmt in enumerate(bank_statements, 1):
    content = f"""BANK STATEMENT

Bank: {stmt['bank']}
Account: {stmt['account']}
Statement Date: March {i}, 2024

Current Balance: ${stmt['balance']}

Recent Transactions:
{chr(10).join(stmt['transactions'])}

This is an official bank statement."""
    
    create_pdf(content, f"files/bank_statement_{i}.pdf")
    create_docx(content, f"files/bank_statement_{i}.docx")

# Create driver's license PDFs and Word docs
for i, lic in enumerate(licenses, 1):
    content = f"""DRIVER LICENSE

State of {lic['state']}
DL Number: {lic['number']}

Name: {lic['name']}
Date of Birth: {lic['dob']}

Class: C
Restrictions: None
Endorsements: None"""
    
    create_pdf(content, f"files/drivers_license_{i}.pdf")
    create_docx(content, f"files/drivers_license_{i}.docx")

print("Created test files in /files directory") 