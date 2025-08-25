import streamlit as st
import csv
import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

try:
    BASE_DIR = os.path.dirname(__file__)
except NameError:
    BASE_DIR = os.getcwd()

CSV_FILE = os.path.join(BASE_DIR, "..", "data", "menu.csv")

def load_menu():
    menu = []
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            name = row[0]
            category = row[1]
            price = float(row[2])
            calories = int(row[3])
            image_url = row[4]
            item_type = row[5]
            menu.append((name, category, price, calories, image_url, item_type))
    return menu

def run_app():
    st.set_page_config(page_title="Restaurant Billing System", layout="wide")

    # Initialize bill number in session
    if "bill_number" not in st.session_state:
        st.session_state.bill_number = 1000

    col_left, col_right = st.columns([1, 3])

    with col_left:
        st.markdown("## 🔍 Search & Filters")
        menu = load_menu()
        search_term = st.text_input("Search Menu Item")
        category_filter = st.selectbox(
            "Select Category",
            ["All"] + sorted(list(set(item[1] for item in menu)))
        )
        type_filter = st.radio("Select Type", ["All", "Veg", "Non-Veg"])

    with col_right:
        st.title("🍽 Restaurant Billing System")

        bill_number = f"BILL-{st.session_state.bill_number}"
        bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"*Bill No:* {bill_number}")
        st.write(f"*Date & Time:* {bill_date}")

        customer_name = st.text_input("Customer Name")
        order_type = st.selectbox("Order Type", ["Dine-in", "Takeaway", "Delivery"])

        # Filtered menu items
        filtered_menu = [
            item for item in menu
            if (category_filter == "All" or item[1] == category_filter)
            and (type_filter == "All" or item[5] == type_filter)
            and (search_term.lower() in item[0].lower())
        ]

        if not filtered_menu:
            st.warning("No items match your filters.")
            return

        if "order" not in st.session_state:
            st.session_state.order = {}

        st.subheader("Menu")
        for name, category, price, calories, image_url, item_type in filtered_menu:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(image_url, width=100)
            with col2:
                st.markdown(f"{name}")
                st.write(f"₹{price:.2f} | {calories} cal | {item_type}")
                qty = st.number_input(
                    f"Quantity for {name}",
                    min_value=0, max_value=20,
                    value=st.session_state.order.get(name, (price, 0))[1],
                    key=f"qty_{name}"
                )
                if qty > 0:
                    st.session_state.order[name] = (price, qty)
                elif name in st.session_state.order:
                    del st.session_state.order[name]

        order = st.session_state.order

        # --- Bill Summary ---
        st.markdown("---")
        st.subheader("🧾 Bill Summary")

        gst_percent = 5  # Fixed GST
        st.write(f"GST: {gst_percent}%")

        discount_percent = st.number_input("Discount (%)", min_value=0, max_value=100, value=0)
        payment_type = st.selectbox("Payment Type", ["Cash", "UPI", "Card"])

        if st.button("Generate Bill"):
            if not order:
                st.error("Please add at least one item to generate a bill.")
                return
            if not customer_name:
                st.error("Please enter customer name.")
                return

            subtotal = sum(price * qty for price, qty in order.values())
            gst_amount = subtotal * (gst_percent / 100)
            discount_amount = subtotal * (discount_percent / 100)
            final_total = subtotal + gst_amount - discount_amount

            # Bill details
            st.write(f"**Customer Name:** {customer_name}")
            st.write(f"**Order Type:** {order_type}")
            st.write(f"**Payment Type:** {payment_type}")

            # Display purchased items table
            st.table(
                [{"Item": item, "Qty": qty, "Price": f"₹{price:.2f}", "Total": f"₹{price * qty:.2f}"}
                 for item, (price, qty) in order.items()]
            )

            st.write(f"**Subtotal:** ₹{subtotal:.2f}")
            st.write(f"**GST ({gst_percent}%):** ₹{gst_amount:.2f}")
            st.write(f"**Discount:** ₹{discount_amount:.2f}")
            st.write(f"**Total:** ₹{final_total:.2f}")

            # --- Download Section ---
            st.markdown("### 📥 Download Bill")
            col_pdf, col_csv, col_json = st.columns(3)

            with col_pdf:
                pdf_buffer = BytesIO()
                c = canvas.Canvas(pdf_buffer, pagesize=letter)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(200, 750, "Restaurant Bill")
                c.setFont("Helvetica", 12)
                c.drawString(50, 730, f"Bill No: {bill_number}")
                c.drawString(50, 715, f"Date: {bill_date}")
                c.drawString(50, 700, f"Customer: {customer_name}")
                c.drawString(50, 685, f"Order Type: {order_type}")
                c.drawString(50, 670, f"Payment Type: {payment_type}")

                y = 640
                c.drawString(50, y, "Item")
                c.drawString(250, y, "Qty")
                c.drawString(300, y, "Price")
                c.drawString(400, y, "Total")
                y -= 20

                for item, (price, qty) in order.items():
                    c.drawString(50, y, item)
                    c.drawString(250, y, str(qty))
                    c.drawString(300, y, f"₹{price:.2f}")
                    c.drawString(400, y, f"₹{price * qty:.2f}")
                    y -= 20

                y -= 10
                c.drawString(50, y, f"Subtotal: ₹{subtotal:.2f}")
                y -= 15
                c.drawString(50, y, f"GST ({gst_percent}%): ₹{gst_amount:.2f}")
                y -= 15
                c.drawString(50, y, f"Discount: ₹{discount_amount:.2f}")
                y -= 15
                c.drawString(50, y, f"Final Total: ₹{final_total:.2f}")
                c.showPage()
                c.save()
                pdf_buffer.seek(0)
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer,
                    file_name=f"bill_{bill_number}.pdf",
                    mime="application/pdf"
                )

            with col_csv:
                csv_data = "Item,Qty,Price,Total\n"
                for item, (price, qty) in order.items():
                    csv_data += f"{item},{qty},{price},{price * qty}\n"
                csv_data += f"\nSubtotal,,,{subtotal}\nGST ({gst_percent}%),,,{gst_amount}\nDiscount,,,{discount_amount}\nFinal Total,,,{final_total}"
                st.download_button(
                    label="Download CSV",
                    data=csv_data.encode("utf-8"),
                    file_name=f"bill_{bill_number}.csv",
                    mime="text/csv"
                )

            with col_json:
                bill_data = {
                    "bill_no": bill_number,
                    "date": bill_date,
                    "customer_name": customer_name,
                    "order_type": order_type,
                    "payment_type": payment_type,
                    "items": [
                        {"name": item, "qty": qty, "price": price, "total": price * qty}
                        for item, (price, qty) in order.items()
                    ],
                    "subtotal": subtotal,
                    "gst": gst_amount,
                    "discount": discount_amount,
                    "final_total": final_total
                }
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(bill_data, indent=4),
                    file_name=f"bill_{bill_number}.json",
                    mime="application/json"
                )

            # Increment bill number for next bill
            st.session_state.bill_number += 1

if __name__ == "__main__":
    run_app()
