from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_invoice_pdf(invoice, items, client, company_settings):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(50, 800, f"Facture n° {invoice.number}")
    c.drawString(50, 780, f"Date: {invoice.date.strftime('%d/%m/%Y')}")
    c.drawString(50, 760, f"Client: {client.first_name} {client.last_name}")
    c.drawString(50, 740, f"Entreprise: {company_settings.company_name}")
    y = 700
    for item in items:
        c.drawString(50, y, f"{item.description} x{item.quantity} - {item.unit_price}€")
        y -= 20
    c.drawString(50, y-20, f"Total: {invoice.total}€")
    c.save()
    buffer.seek(0)
    return buffer
