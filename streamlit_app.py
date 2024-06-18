import streamlit as st
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Google Sheets authentication
SERVICE_ACCOUNT_FILE = 'excel.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1k4UVgLa00Hqa7le3QPbwQMSXwpnYPlvcEQTxXqTEY4U'
SHEET_NAME_1 = 'ZP dane kont'
SHEET_NAME_2 = 'ZP status'

# Authenticate and initialize the Google Sheets client
credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
client = gspread.authorize(credentials)
sheet1 = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME_1)
sheet2 = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME_2)

# Fetch all clients
def fetch_clients():
    clients = []
    rows = sheet1.get_all_values()[1:]  # Skip header row
    for row in rows:
        clients.append(f"{row[1]} {row[0]} {row[3]}")
    return clients

# Function to check if the client already exists
def client_exists(first_name, last_name, phone):
    rows = sheet1.get_all_values()[1:]  # Skip header row
    for row in rows:
        if row[0] == first_name and row[1] == last_name and row[3] == phone:
            return True
    return False

# Function to add a new client to the Google Sheet
def add_client(first_name, last_name, office, phone, email, marital_status, bank_account, swift, tax_office, tax_id, spouse_tax_id):
    if client_exists(first_name, last_name, phone):
        st.error("Taki klient już istnieje")
        return

    new_row = [
        first_name,
        last_name,
        office,
        phone,
        email,
        marital_status,
        bank_account,
        swift,
        tax_office,
        tax_id,
        spouse_tax_id
    ]
    sheet1.append_row(new_row)
    st.success("Nowy klient został dodany")

# Function to add a new service to the Google Sheet
def add_service(client, status_de, year, refund, guardian, remarks, informed, sent, fahrkosten, ubernachtung, entry_24h, entry_8h, entry_kabine, entry_ab_und_an, children, price, status, zapl, payment_method):
    new_row = [
        client,
        status_de,
        year,
        refund,
        guardian,
        remarks,
        informed,
        sent,
        fahrkosten,
        ubernachtung,
        entry_24h,
        entry_8h,
        entry_kabine,
        entry_ab_und_an,
        children,
        price,
        status,
        zapl,
        payment_method,
        datetime.now().strftime("%Y-%m-%d")
    ]
    sheet2.append_row(new_row)
    st.success("Nowa usługa została dodana")

# Main application
def main():
    st.title("System Zarządzania Klientami")

    menu = ["Dodaj klienta", "Dodaj usługę", "Podsumowanie"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Dodaj klienta":
        st.subheader("Dodaj nowego klienta")

        with st.form(key="add_client_form"):
            first_name = st.text_input("Imię")
            last_name = st.text_input("Nazwisko")
            office = st.selectbox("Biuro", ["Przeworsk", "Jarosław"])
            phone = st.text_input("Nr telefonu")
            email = st.text_input("Email")
            marital_status = st.selectbox("Stan cywilny", ["kawaler", "żonaty", "rozwiedziony", "panienka", "mężatka"])
            bank_account = st.text_input("Nr konta bank")
            swift = st.text_input("SWIFT")
            tax_office = st.text_input("Finanzamt")
            tax_id = st.text_input("Nr ID")
            spouse_tax_id = st.text_input("Nr ID małżonka")

            submit_button = st.form_submit_button(label="Dodaj klienta")

        if submit_button:
            add_client(first_name, last_name, office, phone, email, marital_status, bank_account, swift, tax_office, tax_id, spouse_tax_id)

    elif choice == "Dodaj usługę":
        st.subheader("Dodaj nową usługę")

        all_clients = fetch_clients()

        with st.form(key="add_service_form"):
            client = st.selectbox("Klient", all_clients)
            status_de = st.selectbox("Status DE", ["DE - Otrzymano dokumenty", "DE - Rozliczono", "DE - Niekompletny zestaw"])
            year = st.selectbox("Rok", [str(year) for year in range(2019, datetime.now().year)])
            refund = st.text_input("Zwrot")
            guardian = st.selectbox("Opiekun", ["Kamil", "Beata", "Kasia"])
            remarks = st.text_area("Uwagi")
            informed = st.selectbox("Poinformowany", ["Tak", "Nie"])
            sent = st.selectbox("Wysłane", ["Tak", "Nie"])
            fahrkosten = st.text_input("Fahrkosten")
            ubernachtung = st.text_input("Übernachtung")
            entry_24h = st.text_input("24h")
            entry_8h = st.text_input("8h")
            entry_kabine = st.text_input("Kabine")
            entry_ab_und_an = st.text_input("Ab und an")
            children = st.text_area("Dzieci")
            price = st.selectbox("Cena", ["250", "400"])
            status = st.selectbox("Status", ["Opłacony", "Nieopłacony"])
            zapl = st.text_input("Zapłacono")
            payment_method = st.selectbox("Metoda płatności", ["Przelew", "Gotówka"])

            submit_button = st.form_submit_button(label="Dodaj usługę")

        if submit_button:
            add_service(client, status_de, year, refund, guardian, remarks, informed, sent, fahrkosten, ubernachtung, entry_24h, entry_8h, entry_kabine, entry_ab_und_an, children, price, status, zapl, payment_method)

    elif choice == "Podsumowanie":
        st.subheader("Podsumowanie")

        total_clients = len(sheet1.get_all_values()) - 1  # Excluding header row
        total_services = len(sheet2.get_all_values()) - 1  # Excluding header row

        st.write(f"Liczba klientów: {total_clients}")
        st.write(f"Liczba usług: {total_services}")

if __name__ == "__main__":
    main()
