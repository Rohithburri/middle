from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_invoice_pdf(order):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    address = order.address

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, y, "INVOICE")
    y -= 40

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Invoice No: INV-{order.id}")
    y -= 20
    pdf.drawString(50, y, f"Order ID: {order.id}")
    y -= 20
    pdf.drawString(50, y, f"Payment ID: {order.payment_id or '-'}")
    y -= 20
    pdf.drawString(50, y, f"Order Status: {order.status}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Customer Details")
    y -= 25

    pdf.setFont("Helvetica", 11)

    if address:
        pdf.drawString(50, y, f"Name: {address.full_name}")
        y -= 20
        pdf.drawString(50, y, f"Email: {address.email}")
        y -= 20
        pdf.drawString(50, y, f"Phone: {address.phone}")
        y -= 20
        pdf.drawString(50, y, f"Address: {address.address_line1}")
        y -= 20

        if address.address_line2:
            pdf.drawString(50, y, address.address_line2)
            y -= 20

        pdf.drawString(
            50,
            y,
            f"{address.city}, {address.state} - {address.pincode}, {address.country}"
        )
        y -= 40
    else:
        pdf.drawString(50, y, "Address not available")
        y -= 40

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Payment Summary")
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Total Amount: Rs. {order.total}")
    y -= 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Thank you for your order!")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer.getvalue()


def send_invoice_email(order):
    if not order.address:
        raise Exception("Order address not found")

    customer_email = order.address.email

    if not customer_email:
        raise Exception("Customer email not found in address")

    pdf_file = generate_invoice_pdf(order)

    email = EmailMessage(
        subject=f"Invoice for Order #{order.id}",
        body=f"""
Hello {order.address.full_name},

Thank you for your order.

Your payment has been received successfully.
Please find your invoice attached in PDF format.

Order ID: {order.id}
Amount: Rs. {order.total}

Regards,
Eleczo Team
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[customer_email],
    )

    email.attach(
        filename=f"invoice_order_{order.id}.pdf",
        content=pdf_file,
        mimetype="application/pdf"
    )

    email.send(fail_silently=False)

    order.invoice_sent = True
    order.invoice_sent_at = timezone.now()
    order.save(update_fields=["invoice_sent", "invoice_sent_at"])

    return True