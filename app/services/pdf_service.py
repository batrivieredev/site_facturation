from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_invoice_pdf(invoice, items, client, company_settings):
   buffer = io.BytesIO()
   c = canvas.Canvas(buffer, pagesize=A4)
   c.setFont("Helvetica-Bold", 16)
   c.drawString(50, 800, "FACTURE")
   c.setFont("Helvetica", 12)
   c.drawString(400, 800, f"Numéro : {invoice.number}")
   c.drawString(400, 785, f"Date d'émission : {invoice.date.strftime('%d/%m/%Y')}")
   # Bloc entreprise
   c.setFont("Helvetica-Bold", 12)
   c.drawString(50, 770, "Entreprise :")
   c.setFont("Helvetica", 12)
   c.drawString(50, 755, f"{company_settings.company_name} (EI / Auto-entrepreneur)")
   c.drawString(50, 740, f"{company_settings.first_name} {company_settings.last_name}")
   c.drawString(50, 725, f"{company_settings.address}")
   c.drawString(50, 710, f"Tél : {company_settings.phone}")
   c.drawString(50, 695, f"Email : {company_settings.email}")
   c.drawString(50, 680, f"SIRET : {company_settings.siret}")
   # Bloc client
   c.setFont("Helvetica-Bold", 12)
   c.drawString(350, 770, "Client :")
   c.setFont("Helvetica", 12)
   c.drawString(350, 755, f"{client.last_name} {client.first_name}")
   c.drawString(350, 740, f"{client.address}")
   c.drawString(350, 725, f"Tél : {client.phone}")
   c.drawString(350, 710, f"Email : {client.email}")
   # Tableau facturation
   c.setFont("Helvetica-Bold", 12)
   c.drawString(50, 670, "Désignation")
   c.drawString(200, 670, "Type de RDV")
   c.drawString(300, 670, "Durée")
   c.drawString(370, 670, "Prix unitaire")
   c.drawString(470, 670, "Quantité")
   c.drawString(540, 670, "Total")
   c.setFont("Helvetica", 12)
   y = 650
   for item in items:
       c.drawString(50, y, f"Séance de {item.description}")
       c.drawString(200, y, f"{item.description}")
       c.drawString(300, y, f"{getattr(item, 'duration', '')} min")
       c.drawString(370, y, f"{item.unit_price} €")
       c.drawString(470, y, f"{item.quantity}")
       c.drawString(540, y, f"{item.total} €")
       y -= 20
   # Totaux
   c.setFont("Helvetica-Bold", 12)
   c.drawString(370, y-10, "Total HT :")
   c.drawString(470, y-10, f"{invoice.total} €")
   c.setFont("Helvetica", 12)
   c.drawString(370, y-30, "TVA :")
   c.drawString(470, y-30, "0 € – TVA non applicable, art. 293B du CGI")
   c.setFont("Helvetica-Bold", 12)
   c.drawString(370, y-50, "Total à payer :")
   c.drawString(470, y-50, f"{invoice.total} €")
   # Mentions
   c.setFont("Helvetica", 10)
   c.drawString(50, y-80, "TVA non applicable, article 293B du CGI")
   c.drawString(50, y-100, "Conditions de paiement : paiement comptant")
   c.drawString(50, y-115, "Moyen de paiement : espèces, chèque, virement")
   c.drawString(50, y-130, "Mention légale EI : EI / Auto-entrepreneur")
   c.drawString(50, y-145, f"Contact : {company_settings.email} / {company_settings.phone}")
   # Numéro de page
   c.setFont("Helvetica", 9)
   c.drawRightString(570, 30, "Page 1/1")
   c.save()
   buffer.seek(0)
   return buffer
