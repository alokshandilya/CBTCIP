from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


def create_receipt(filename, transaction_details, company_details):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Monospace font for the entire document
    c.setFont("Courier", 12)

    # Draw header
    def draw_header():
        c.setFont("Courier-Bold", 24)
        c.drawString(200, height - 50, "Payment Receipt")
        c.setFont("Courier", 12)
        c.drawString(50, height - 80, company_details["name"])
        c.drawString(50, height - 95, company_details["address"])
        c.drawString(50, height - 110, company_details["city"])
        c.drawString(50, height - 125, f"Phone: {company_details['phone']}")
        c.line(50, height - 130, width - 50, height - 130)

    # Draw footer
    def draw_footer():
        c.setFont("Courier-Oblique", 10)
        c.drawString(50, 30, "Thank you for your business!")
        c.drawString(
            50, 15, f"For any queries, contact us at {company_details['phone']}"
        )

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


def main():
    company_details = {
        "name": input("Enter company name: "),
        "address": input("Enter company address: "),
        "city": input("Enter company city, state, ZIP code: "),
        "phone": input("Enter company phone number: "),
    }

    transaction_details = {
        "receipt_number": input("Enter receipt number: "),
        "customer_name": input("Enter customer name: "),
        "customer_address": input("Enter customer address: "),
        "customer_phone": input("Enter customer phone number: "),
        "items": [],
        "total_amount": 0.0,
    }

    while True:
        description = input("Enter item description (or 'done' to finish): ")
        if description.lower() == "done":
            break
        quantity = int(input("Enter item quantity: "))
        unit_price = float(input("Enter item unit price: "))
        total = quantity * unit_price
        transaction_details["items"].append(
            {
                "description": description,
                "quantity": quantity,
                "unit_price": unit_price,
                "total": total,
            }
        )
        transaction_details["total_amount"] += total

    filename = input("Enter filename for the receipt (e.g., 'receipt.pdf'): ")
    create_receipt(filename, transaction_details, company_details)
    print(f"Receipt saved as {filename}")


if __name__ == "__main__":
    main()
