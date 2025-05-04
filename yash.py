import streamlit as st
import pandas as pd
import hashlib

st.title("Store Sales Ledger with Hashing")

# Input section
with st.form("sales_form"):
    date = st.date_input("Date")
    invoice = st.text_input("Invoice No.")
    customer = st.text_input("Customer Name")
    item = st.text_input("Item Sold")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    unit_price = st.number_input("Unit Price", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Entry")

# Session state to store entries
if "ledger" not in st.session_state:
    st.session_state.ledger = []

if submitted:
    total = quantity * unit_price
    entry = {
        "Date": str(date),
        "Invoice No.": invoice,
        "Customer": customer,
        "Item Sold": item,
        "Quantity": quantity,
        "Unit Price": unit_price,
        "Total Amount": total,
    }
    st.session_state.ledger.append(entry)

# Display ledger
if st.session_state.ledger:
    df = pd.DataFrame(st.session_state.ledger)

    # Add row hashes
    def hash_row(row):
        return hashlib.sha256(''.join(map(str, row.values)).encode()).hexdigest()

    df["Row Hash"] = df.apply(hash_row, axis=1)
    st.dataframe(df)

    # Show total
    st.subheader(f"Total Sales: ${df['Total Amount'].sum():.2f}")
