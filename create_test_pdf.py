from fpdf import FPDF

def create_invoice_pdf(output_file="test_invoice.pdf"):
    # Create PDF object
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", size=12)
    
    # Read the invoice text
    with open("test_invoice.txt", "r") as f:
        lines = f.readlines()
    
    # Add content to PDF
    for line in lines:
        pdf.cell(200, 10, txt=line.strip(), ln=True, align='L')
    
    # Save the PDF
    pdf.output(output_file)

if __name__ == "__main__":
    create_invoice_pdf() 