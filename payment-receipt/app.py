from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


def create_receipt(filename, transaction_details):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(200, 750, "Payment Receipt")

    # Company Information
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "Company Name")
    c.drawString(50, 685, "1234 Main Street")
    c.drawString(50, 670, "City, State ZIP Code")
    c.drawString(50, 655, "Phone: (123) 456-7890")

    # Receipt Details
    c.drawString(400, 700, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(400, 685, f"Receipt #: {transaction_details['receipt_number']}")

    # Customer Information
    c.drawString(50, 620, "Bill To:")
    c.drawString(50, 605, transaction_details["customer_name"])
    c.drawString(50, 590, transaction_details["customer_address"])
    c.drawString(50, 575, transaction_details["customer_phone"])

    # Itemized List
    c.drawString(50, 540, "Description")
    c.drawString(200, 540, "Quantity")
    c.drawString(300, 540, "Unit Price")
    c.drawString(400, 540, "Total")

    y = 520
    for item in transaction_details["items"]:
        c.drawString(50, y, item["description"])
        c.drawString(200, y, str(item["quantity"]))
        c.drawString(300, y, f"${item['unit_price']:.2f}")
        c.drawString(400, y, f"${item['total']:.2f}")
        y -= 20

    # Total Amount
    c.drawString(300, y - 20, "Total Amount:")
    c.drawString(400, y - 20, f"${transaction_details['total_amount']:.2f}")

    # Footer
    c.drawString(50, 100, "Thank you for your business!")

    c.save()


# Example transaction details
transaction_details = {
    "receipt_number": "123456789",
    "customer_name": "John Doe",
    "customer_address": "5678 Elm Street",
    "customer_phone": "(987) 654-3210",
    "items": [
        {"description": "Widget A", "quantity": 2, "unit_price": 25.00, "total": 50.00},
        {"description": "Widget B", "quantity": 1, "unit_price": 15.00, "total": 15.00},
    ],
    "total_amount": 65.00,
}

create_receipt("receipt.pdf", transaction_details)
