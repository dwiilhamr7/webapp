import streamlit as st
from sqlalchemy import text

list_room = ['', 'twin_deluxe', 'double_bed', 'premium_intermediate', 'business_premium', 'diamond_class', 'Paket_Request']
list_gender = ['', 'male', 'female']
list_payment = ['', 'ATM', 'Transfer', 'Tunai']
list_metode = ['','Diantar', 'Ditunggu']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwiilhamr07:QBZxK7A6gYND@ep-hidden-unit-18107709.us-east-2.aws.neon.tech/web")

st.header('Diamond Luxury Tower Hotel')
page_akhir = st.sidebar.selectbox("Restaurant Hotel", ["Database Restaurant","Additing Pelanggan"])

with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS hotel_restaurant (id serial, pelanggan text, makanan varchar, jumlah_makanan text, minuman varchar, \
                                                       jumlah_minuman text, metode text, no_tempat text, total_harga text, pembayaran text, tanggal date);')
    session.execute(query)

if page_akhir == "Database Restaurant":
    data = conn.query('SELECT * FROM hotel_restaurant ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page_akhir == "Additing Pelanggan":
    if st.button('Additing'):
       with conn.session as session:
                query_restaurant = text('INSERT INTO hotel_restaurant ("pelanggan", "makanan", "jumlah_makanan", "minuman", "jumlah_minuman", "metode", "no_tempat", "total_harga", "pembayaran", "tanggal") \
                        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10);')
                session.execute(query_restaurant, {'1':'', '2':None, '3':0, '4':None, '5':0, '6':'', '7':'', '8':0, '9':'', '10':''})
                session.commit()

    data = conn.query('SELECT * FROM hotel_restaurant ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        pelanggan_awal = result.loc["pelanggan"]
        makanan_awal = result["makanan"]
        jumlah_makanan_awal = result["jumlah_makanan"]
        minuman_awal = result["minuman"]
        jumlah_minuman_awal = result["jumlah_minuman"]
        metode_awal = result["metode"]
        no_tempat_awal = result["no_tempat"]
        total_harga_awal = result["total_harga"]
        pembayaran_awal = result["pembayaran"]
        tanggal_awal = result["tanggal"]

        with st.expander(f'a.n. {pelanggan_awal}'):
            with st.form(f'data-{id}'):
                pelanggan_akhir = st.text_input("nama", pelanggan_awal)
                makanan_akhir = st.text_input("makanan", makanan_awal)
                jumlah_makanan_akhir = st.text_input("jumlah_makanan", jumlah_makanan_awal)
                minuman_akhir = st.text_input("minuman", minuman_awal) 
                jumlah_minuman_akhir = st.text_input("jumlah_minuman", jumlah_minuman_awal)
                metode_akhir = st.selectbox("metode", list_metode, list_metode.index(metode_awal))
                no_tempat_akhir = st.text_input("no_tempat", no_tempat_awal)
                total_harga_akhir = st.text_input("total_harga", total_harga_awal)
                pembayaran_akhir = st.selectbox("pembayaran", list_payment, list_payment.index(pembayaran_awal))
                tanggal_akhir = st.date_input("tanggal",tanggal_awal)

                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE hotel_restaurant \
                                          SET pelanggan=:1, makanan=:2, jumlah_makanan=:3, minuman=:4, jumlah_minuman=:5 \
                                          metode=:6, no_tempat=:7, total_harga=:8, pembayaran=:9, tanggal=:10\
                                          WHERE id=:10;')
                            session.execute(query, {'1':pelanggan_akhir, '2':makanan_akhir, '3':jumlah_makanan_akhir, '4':minuman_akhir, '5':jumlah_minuman_akhir, 
                                                    '6':metode_akhir, '7':no_tempat_akhir, '8':total_harga_akhir, '9':pembayaran_akhir, '10':tanggal_akhir, '11':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM hotel_restaurant WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()