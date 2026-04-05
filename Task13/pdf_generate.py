from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path
from datetime import datetime

def generate_pdf(data, output_name):
    output_path = Path("reports") / output_name
    c = canvas.Canvas(str(output_path), pagesize=letter)
    width, height = letter
    y = height - 50
    
    #Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, y, "Monthly Sales Report")
    y -= 40

    # Summary
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Month: {data['month']}")
    y -= 20
    c.drawString(50, y, f"Total Revenue: {data['revenue']}")
    y -= 20
    c.drawString(50, y, f"Units Sold: {data['units']}")
    y -= 40

    # Conditional warning
    if data["warning"]:
        c.setFillColorRGB(1, 0, 0)
        c.drawString(50, y, "Warning: West region declining!")
        c.setFillColorRGB(0, 0, 0)

    # Footer
    c.drawString(
        50,
        50,
        f"Generated: {datetime.now()}"
    )

    c.save()

    return output_path