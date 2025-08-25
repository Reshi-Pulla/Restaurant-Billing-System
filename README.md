# 🍽 Restaurant Billing System

## 📌 Overview
The **Restaurant Billing System** is a Streamlit-based application designed to streamline restaurant order management and billing.  
It allows searching and filtering menu items, creating orders, applying discounts, calculating GST, and downloading bills in **PDF**, **CSV**, or **JSON** formats.  
This project was built as part of the **Broskieshub Internship Program**.

---

## 🛠 Tools & Technologies Used

- **[Python 3.x](https://www.python.org/)** – Core programming language for backend logic.
- **[Streamlit](https://streamlit.io/)** – Framework for building interactive web apps.
- **[Pandas](https://pandas.pydata.org/)** – Data handling and CSV file operations.
- **[FPDF](https://pyfpdf.readthedocs.io/en/latest/)** – For generating PDF bills.
- **[JSON](https://www.json.org/)** – For saving and reading bill data in JSON format.
- **[CSV](https://docs.python.org/3/library/csv.html)** – For storing bill data in spreadsheet format.
- **[ReportLab](https://www.reportlab.com/)** – Additional PDF generation and formatting (if used).
- **[VS Code](https://code.visualstudio.com/)** – Code editor used for development.
- **[Git](https://git-scm.com/)** – Version control system for managing source code.

---

## ✨ Features
- **Menu Search & Filters**
  - Search menu items by name.
  - Filter by category (Starters, Main Course, Desserts, etc.).
  - Filter by type (Veg / Non-Veg).

- **Order Management**
  - Select quantities for multiple items.
  - Auto-calculates totals.
  - Fixed **GST (5%)**.
  - Optional discount input.
  - Auto-increment bill numbers.

- **Bill Summary**
  - Captures customer details and payment method.
  - Displays purchased items in a table.
  - Shows subtotal, GST, discount, and final payable amount.
  

- **Bill Export**
  - Download bill in **PDF**, **CSV**, or **JSON** format.
  - Files can be saved manually into the `bills/` folder.

---

## 🗂 Folder Structure
```

RESTAURANT_BILLING/
│
├── .streamlit/
│   └── config.toml
│
├── bills/
│   ├── bill_BILL-1000.csv
│   ├── bill_BILL-1000.json
│   └── bill_BILL-1000.pdf
│
├── data/
│   └── menu.csv
│
├── db/
│   └── restaurant.db
│
├── images/
│
├── ui/
│   ├── __pycache__/
│   ├── billing_ui.py
│   └── main_ui.py
│
├── utils/
│   ├── __pycache__/
│   ├── calculator.py
│   └── db_utils.py
│
├── app.py
├── README.md

````

---

## 🛠 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repo-url>
   cd restaurant-billing
   ````

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   ```bash
   streamlit run app.py
   ```

---

## 💡 Usage

1. Launch the application using Streamlit.
2. Use the search bar or filters to find menu items.
3. Select quantities for the items you want to order.
4. Enter customer details, payment method, and discount (optional).
5. Click **Generate Bill** to view the bill summary.
6. Choose a format (**PDF**, **CSV**, or **JSON**) and click **Download**.
7. Save the bill manually to the `bills/` folder.

---



