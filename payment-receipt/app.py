from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


def create_receipt(filename, transaction_details):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Monospace font for the entire document
    c.setFont("Courier", 12)

    # Draw header
    def draw_header():
        c.setFont("Courier-Bold", 24)
        c.drawString(200, height - 50, "Payment Receipt")
        c.setFont("Courier", 12)
        c.drawString(50, height - 80, "Company Name")
        c.drawString(50, height - 95, "1234 Main Street")
        c.drawString(50, height - 110, "City, State ZIP Code")
        c.drawString(50, height - 125, "Phone: (123) 456-7890")
        c.line(50, height - 130, width - 50, height - 130)

    # Draw footer
    def draw_footer():
        c.setFont("Courier-Oblique", 10)
        c.drawString(50, 30, "Thank you for your business!")
        c.drawString(50, 15, "For any queries, contact us at (123) 456-7890")

    # Draw item table
    def draw_item_table(items, y_start):
        c.setFont("Courier-Bold", 12)
        c.drawString(50, y_start, "Description")
        c.drawString(250, y_start, "Quantity")
        c.drawString(350, y_start, "Unit Price")
        c.drawString(450, y_start, "Total")
        c.line(50, y_start - 5, 500, y_start - 5)

        y = y_start - 20
        c.setFont("Courier", 12)
        for item in items:
            c.drawString(50, y, item["description"])
            c.drawString(250, y, str(item["quantity"]))
            c.drawString(350, y, f"${item['unit_price']:.2f}")
            c.drawString(450, y, f"${item['total']:.2f}")
            y -= 20

        return y

    # Draw header
    draw_header()

    # Receipt and Customer Details
    c.setFont("Courier", 12)
    c.drawString(400, height - 80, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(
        400, height - 95, f"Receipt #: {transaction_details['receipt_number']}"
    )
    c.drawString(50, height - 160, "Bill To:")
    c.drawString(50, height - 175, transaction_details["customer_name"])
    c.drawString(50, height - 190, transaction_details["customer_address"])
    c.drawString(50, height - 205, transaction_details["customer_phone"])

    # Item table
    y = draw_item_table(transaction_details["items"], height - 230)

    # Total Amount
    c.setFont("Courier-Bold", 12)
    c.drawString(350, y - 20, "Total Amount:")
    c.drawString(450, y - 20, f"${transaction_details['total_amount']:.2f}")

    # Draw footer
    draw_footer()

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
