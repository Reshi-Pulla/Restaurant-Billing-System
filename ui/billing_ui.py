import os
import json
import csv
import streamlit as st
from fpdf import FPDF

# --- Folder for saving bills ---
BILL_FOLDER = os.path.join(os.getcwd(), "bills")
os.makedirs(BILL_FOLDER, exist_ok=True)

# --- Session State Setup ---
if "bill_number" not in st.session_state:
    st.session_state.bill_number = 1
if "items" not in st.session_state:
    st.session_state.items = []

# --- App Title ---
st.title("🧾 Billing System")

# --- Input Fields ---
col1, col2, col3 = st.columns(3)
with col1:
    item_name = st.text_input("Item Name")
with col2:
    qty = st.number_input("Quantity", min_value=1, value=1)
with col3:
    price = st.number_input("Price", min_value=0.0, value=0.0, format="%.2f")

if st.button("Add Item"):
    if item_name and price > 0:
        st.session_state.items.append({
            "name": item_name,
            "qty": qty,
            "price": price,
            "total": qty * price
        })
    else:
        st.warning("Please enter a valid item name and price.")

# --- Display Items ---
if st.session_state.items:
    st.subheader("Items Purchased")
    st.table(st.session_state.items)

    subtotal = sum(item["total"] for item in st.session_state.items)
    gst = subtotal * 0.05  # Fixed 5% GST
    total_amount = subtotal + gst

    st.write(f"**Subtotal:** ₹{subtotal:.2f}")
    st.write(f"**GST (5%):** ₹{gst:.2f}")
    st.write(f"**Total Amount:** ₹{total_amount:.2f}")

    # --- Generate Bill Files ---
    bill_number = st.session_state.bill_number
    bill_data = {
        "bill_number": bill_number,
        "items": st.session_state.items,
        "subtotal": subtotal,
        "gst": gst,
        "total": total_amount
    }

    # File paths
    pdf_path = os.path.join(BILL_FOLDER, f"bill_{bill_number}.pdf")
    json_path = os.path.join(BILL_FOLDER, f"bill_{bill_number}.json")
    csv_path = os.path.join(BILL_FOLDER, f"bill_{bill_number}.csv")

    # Save JSON
    with open(json_path, "w") as f:
        json.dump(bill_data, f, indent=4)

    # Save CSV
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Item", "Quantity", "Price", "Total"])
        for item in st.session_state.items:
            writer.writerow([item["name"], item["qty"], item["price"], item["total"]])
        writer.writerow(["", "", "Subtotal", subtotal])
        writer.writerow(["", "", "GST (5%)", gst])
        writer.writerow(["", "", "Total", total_amount])

    # Save PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Bill No: {bill_number}", ln=True, align="C")
    pdf.cell(200, 10, "Purchased Items", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    for item in st.session_state.items:
        pdf.cell(0, 10, f"{item['name']} - {item['qty']} x ₹{item['price']} = ₹{item['total']}", ln=True)
    pdf.cell(0, 10, f"Subtotal: ₹{subtotal:.2f}", ln=True)
    pdf.cell(0, 10, f"GST (5%): ₹{gst:.2f}", ln=True)
    pdf.cell(0, 10, f"Total: ₹{total_amount:.2f}", ln=True)
    pdf.output(pdf_path)

    # --- Download Buttons in One Row ---
    st.subheader("Download Bill")
    col_pdf, col_json, col_csv = st.columns(3)
    with col_pdf:
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name=f"bill_{bill_number}.pdf", mime="application/pdf")
    with col_json:
        with open(json_path, "rb") as f:
            st.download_button("Download JSON", f, file_name=f"bill_{bill_number}.json", mime="application/json")
    with col_csv:
        with open(csv_path, "rb") as f:
            st.download_button("Download CSV", f, file_name=f"bill_{bill_number}.csv", mime="text/csv")

    # Increment bill number for next bill
    if st.button("Finish Bill"):
        st.session_state.bill_number += 1
        st.session_state.items = []

