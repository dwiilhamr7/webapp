import streamlit as st
from sqlalchemy import text

list_room = ['', 'twin_deluxe', 'double_bed', 'premium_intermediate', 'business_premium', 'diamond_class', 'Paket_Request']
list_gender = ['', 'male', 'female']
list_payment = ['', 'ATM', 'Transfer', 'Tunai']
list_metode = ['','Diantar', 'Ditunggu']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwiilhamr07:QBZxK7A6gYND@ep-hidden-unit-18107709.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS hotel_restaurant (id serial, pelanggan text, makanan varchar, jumlah_makanan integer, minuman varchar, \
                                                       jumlah_minuman integer, metode text, no_tempat text, total_harga integer, pembayaran text);')
    session.execute(query)

st.header('Diamond Luxury Tower Hotel')
page_akhir = st.sidebar.selectbox("Restaurant Hotel", ["Database Restaurant","Additing Pelanggan"])

if page_akhir == "Database Restaurant":
    data = conn.query('SELECT * FROM hotel_restaurant ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page_akhir == "Additing Pelanggan":
    if st.button('Additing'):
       with conn.session as session:
                query_restaurant = text('INSERT INTO hotel_restaurant ("pelanggan", "makanan", "jumlah_makanan", "minuman", "jumlah_minuman", "metode", "no_tempat", "total_harga", "pembayaran") \
                        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9);')
                session.execute(query_restaurant, {'1':'', '2':None, '3':0, '4':None, '5':0, '6':'', '7':'', '8':0, '9':''})
                session.commit()

    data = conn.query('SELECT * FROM hotel_restaurant ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        pelanggan_lama = result.loc["pelanggan"]
        makanan_lama = result["makanan"]
        jumlah_makanan_lama = result["jumlah_makanan"]
        minuman_lama = result["minuman"]
        jumlah_minuman_lama = result["jumlah_minuman"]
        metode_lama = result["metode"]
        no_tempat_lama = result["no_tempat"]
        total_harga_lama = result["total_harga"]
        pembayaran_lama = result["pembayaran"]

        with st.expander(f'a.n. {pelanggan_lama}'):
            with st.form(f'data-{id}'):
                pelanggan_baru = st.text_input("nama", pelanggan_lama)
                makanan_baru = st.text_input("makanan", makanan_lama)
                jumlah_makanan_baru = st.text_input("jumlah_makanan", jumlah_makanan_lama)
                minuman_baru = st.text_input("minuman", minuman_lama) 
                jumlah_minuman_baru = st.text_input("jumlah_minuman", jumlah_minuman_lama)
                metode_baru = st.selectbox("metode", list_metode, list_metode.index(metode_lama))
                no_tempat_baru = st.text_input("no_tempat", no_tempat_lama)
                total_harga_baru = st.text_input("total_harga", total_harga_lama)
                pembayaran_baru = st.selectbox("pembayaran", list_payment, list_payment.index(pembayaran_lama))

                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE hotel_restaurant \
                                          SET pelanggan=:1, makanan=:2, jumlah_makanan=:3, minuman=:4, jumlah_minuman=:5 \
                                          metode=:6, no_tempat=:7, total_harga=:8, pembayaran=:9, \
                                          WHERE id=:10;')
                            session.execute(query, {'1':pelanggan_baru, '2':makanan_baru, '3':jumlah_makanan_baru, '4':minuman_baru, '5':jumlah_minuman_baru, 
                                                    '6':metode_baru, '7':no_tempat_baru, '8':total_harga_baru, '9':pembayaran_baru, '10':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM hotel_restaurant WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()