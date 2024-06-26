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
        if company_details["city"]:
            c.drawString(50, height - 110, company_details["city"])
        if company_details["zip_code"]:
            c.drawString(50, height - 125, company_details["zip_code"])
        c.drawString(50, height - 140, f"Phone: {company_details['phone']}")
        c.line(50, height - 150, width - 50, height - 150)

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


def get_company_details():
    print("Enter company details:")
    name = input("Company Name: ")
    address_city_zip = input("Company Address (City, State, ZIP Code): ")
    phone = input("Company Phone Number: ")

    # Splitting the address, city, and ZIP code based on the input format
    parts = address_city_zip.split(",")
    if len(parts) >= 2:
        address = parts[0].strip()
        city = parts[1].strip()
        # Combining the rest of the parts back into the ZIP code
        zip_code = ",".join(parts[2:]).strip()
    else:
        address = address_city_zip.strip()
        city = ""
        zip_code = ""

    return {
        "name": name,
        "address": address,
        "city": city,
        "zip_code": zip_code,
        "phone": phone,
    }


def get_transaction_details():
    print("\nEnter transaction details:")
    receipt_number = input("Receipt Number: ")
    customer_name = input("Customer Name: ")
    customer_address = input("Customer Address: ")
    customer_phone = input("Customer Phone Number: ")

    items = []
    total_amount = 0.0
    while True:
        description = input("\nEnter item description (or 'done' to finish): ")
        if description.lower() == "done":
            break
        quantity = int(input("Quantity: "))
        unit_price = float(input("Unit Price: "))
        total = quantity * unit_price
        total_amount += total

        items.append(
            {
                "description": description,
                "quantity": quantity,
                "unit_price": unit_price,
                "total": total,
            }
        )

    return {
        "receipt_number": receipt_number,
        "customer_name": customer_name,
        "customer_address": customer_address,
        "customer_phone": customer_phone,
        "items": items,
        "total_amount": total_amount,
    }


def main():
    company_details = get_company_details()
    transaction_details = get_transaction_details()

    filename = input("\nEnter filename for the receipt (e.g., 'receipt.pdf'): ")
    create_receipt(filename, transaction_details, company_details)
    print(f"\nReceipt saved as {filename}")


if __name__ == "__main__":
    main()
