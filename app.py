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
        
        data = conn.query('SELECT * FROM RESERVATION ORDER By id;', ttl="0")
        for _, result in data.iterrows():        
            id = result['id']
            nama_lama = result["nama"]
            gender_lama = result["gender"]
            contact_lama = result["contact"]
            series_room_lama = result["series_room"]
            other_needs_lama = result["other_needs"]
            check_in_lama = result["check_in"]
            time_ci_lama = result["time_ci"]
            check_out_lama = result["check_out"]
            time_co_lama = result["time_co"]
            payment_lama = result["payment"]
            price_lama = result["price"]

        with st.expander(f'a.n. {patient_name_lama}'):
            with st.form(f'data-{id}'):
                nama_baru = st.text_input("nama", nama_lama)
                gender_baru = st.selectbox("gender", list_gender, list_gender.index(gender_lama))
                contact_baru = st.text_input("contact", contact_lama)
                series_room_baru = st.multiselect("series_room", ['Twin Deluxe', 'Double Bed', 'Premium Business', 'Family Class', 'Business VVIP'], eval(series_room_lama))
                other_needs_baru = st.text_input("other_needs", other_needs_lama)
                check_in_baru = st.date_input("check_in", check_in_lama)
                time_ci_baru = st.time_input("time_ci", time_ci_lama)
                check_out_baru = st.date_input("check_out", check_out_lama)
                time_co_baru = st.date_input("time_co", time_co_lama)
                payment_baru = st.selectbox("payment", list_payment, list_payment.index(payment_lama))
                price_baru = st.text_input("price", price_lama)

                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE RESERVATION \
                                          SET nama=:1, gender=:2, contact=:3, series_room=:4, other_needs=:5, \
                                          check_in=:6, time_ci=:7, check_out=:8, time_co=:9, paymen=:10, price=:11, \
                                          WHERE id=:12;')
                            session.execute(query, {'1':nama_baru, '2':gender_baru, '3':contact_baru, '4':str(series_room_baru), '5':other_needs_baru,
                                                    '6':check_in_baru, '7':time_ci_baru, '8':check_out_baru, '9':time_co_baru, '10':payment_baru, '11':price, '12':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM RESERVATION WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()