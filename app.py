import streamlit as st
import pandas as pd
from sqlalchemy import text

# Data reservasi
data_reservasi = pd.DataFrame({
    'Pertanyaan': ['Nama', 'Makan:', 'Minum:', 'Pembayaran:', 'No Kamar:', 'No Meja:'],
    'Type': ['text', 'chose multiple', 'chose multiple', 'chose bersyarat', 'text', 'text'],  # Mengubah tipe data menjadi text
    'Harga': [None, {'Nasi Goreng': 22000, 'Mie Goreng': 10000, 'Ayam Goreng': 15000}, {'Es Teh': 8000, 'Es Jeruk': 8000, 'Air Mineral': 5000}, None, None, None],
    'Value': [None, None, None, None, None, None]
})

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwiilhamr07:QBZxK7A6gYND@ep-hidden-unit-18107709.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS RESERVATION (id serial, \
                                                       Nama varchar, \
                                                       Makan text[], \
                                                       Minum text[], \
                                                       Pembayaran varchar, \
                                                       No_Kamar varchar, \
                                                       No_Meja varchar, \
                                                       PRIMARY KEY (id));')
    session.execute(query)

# Tampilkan form untuk mengisi data
st.header('CAFE HOTEL NUANSA LIMA')
page = st.sidebar.selectbox("Reservasi Cafe", ["View Data", "Edit Data"])

if page == "View Data":
    # Dummy data untuk ditampilkan
    dummy_data = [
        {'Nama': 'John Doe', 'Makan': ['Nasi Goreng', 'Ayam Goreng'], 'Minum': ['Es Teh', 'Air Mineral'], 'Pembayaran': 'Debit', 'No Kamar': '101', 'No Meja': 'A1', 'Total Harga': 27000},
        {'Nama': 'Jane Doe', 'Makan': ['Mie Goreng', 'Ayam Goreng'], 'Minum': ['Es Jeruk', 'Air Mineral'], 'Pembayaran': 'Cash', 'No Kamar': '102', 'No Meja': 'A2', 'Total Harga': 28000},
    ]

    # Tampilkan data dalam bentuk tabel
    st.subheader('Data Reservasi')
    st.table(dummy_data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        st.subheader('Form Reservasi')
        total_harga = 0  # Inisialisasi total harga

        for _, row in data_reservasi.iterrows():
            pertanyaan = row['Pertanyaan']
            tipe_data = row['Type']

            if tipe_data == 'text':
                jawaban = st.text_input(pertanyaan, key=f"{pertanyaan.strip(':')}_input")
            elif tipe_data == 'integer':
                jawaban = st.number_input(pertanyaan, key=f"{pertanyaan.strip(':')}_input")
            elif tipe_data == 'chose multiple':
                pilihan = row['Harga'].keys()  # Mengambil pilihan dari kolom Harga
                jawaban = st.multiselect(pertanyaan, pilihan, key=f"{pertanyaan.strip(':')}_input")
            elif tipe_data == 'chose bersyarat':
                pilihan = ['Cash', 'Debit']  # Ganti dengan pilihan yang sesuai
                jawaban = st.selectbox(pertanyaan, pilihan, key=f"{pertanyaan.strip(':')}_input")

            # Update nilai di dalam data
            data_reservasi.at[_, 'Value'] = jawaban

            # Hitung total harga makanan dan minuman
            if pertanyaan == 'Makan:':
                total_harga += sum([row['Harga'][makanan] for makanan in jawaban])
            elif pertanyaan == 'Minum:':
                total_harga += sum([row['Harga'][minuman] for minuman in jawaban])

        # Menampilkan total harga
        st.write(f"Total Harga: {total_harga}")

        # Tombol untuk menyimpan data reservasi
        if st.button('Reservasi'):
            st.success('Data reservasi berhasil disimpan!')