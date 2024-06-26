from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"


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
        c.drawString(50, height - 80, transaction_details["company_name"])
        c.drawString(50, height - 95, transaction_details["company_address"])
        c.drawString(50, height - 110, f"Phone: {transaction_details['company_phone']}")
        c.line(50, height - 130, width - 50, height - 130)

    # Draw footer
    def draw_footer():
        c.setFont("Courier-Oblique", 10)
        c.drawString(50, 30, "Thank you for your business!")
        c.drawString(
            50,
            15,
            f"For any queries, contact us at {transaction_details['company_phone']}",
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


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/generate_receipt", methods=["POST"])
def generate_receipt():
    try:
        company_name = request.form["company_name"]
        company_address = request.form["company_address"]
        company_phone = request.form["company_phone"]
        receipt_number = request.form["receipt_number"]
        customer_name = request.form["customer_name"]
        customer_address = request.form["customer_address"]
        customer_phone = request.form["customer_phone"]

        items = []
        total_amount = 0
        for i in range(1, int(request.form["item_count"]) + 1):
            description = request.form[f"item{i}_description"]
            quantity = int(request.form[f"item{i}_quantity"])
            unit_price = float(request.form[f"item{i}_unit_price"])
            total = quantity * unit_price
            total_amount += total

            item = {
                "description": description,
                "quantity": quantity,
                "unit_price": unit_price,
                "total": total,
            }
            items.append(item)

        transaction_details = {
            "company_name": company_name,
            "company_address": company_address,
            "company_phone": company_phone,
            "receipt_number": receipt_number,
            "customer_name": customer_name,
            "customer_address": customer_address,
            "customer_phone": customer_phone,
            "items": items,
            "total_amount": total_amount,
        }

        receipt_filename = os.path.join("static", "receipt.pdf")
        create_receipt(receipt_filename, transaction_details)
        return send_file(receipt_filename, as_attachment=True)
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for("form"))


if __name__ == "__main__":
    app.run(debug=True)
