import streamlit as st
from sqlalchemy import text

list_room = ['', 'twin deluxe', 'double bed', 'premium intermediate', 'business premium', 'diamond class', 'Paket Request']
list_gender = ['', 'male', 'female']
list_payment = ['', 'ATM', 'Transfer', 'Tunai']
list_metode = ['','Diantar', 'Ditunggu']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwiilhamr07:QBZxK7A6gYND@ep-hidden-unit-18107709.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS hotel_room (id serial, nama text, gender char(25), contact text, series_hotel_room text, other_needs text, \
                                                       check_in date, time_ci text, check_out date, time_co text, payment text, price text);')
    query = text('CREATE TABLE IF NOT EXISTS hotel_restaurant (id serial, pelanggan text, makanan varchar, jumlah_makanan integer, minuman varchar, \
                                                       jumlah_minuman integer, metode text, no_tempat text, total_harga integer, pembayaran text);')
    session.execute(query)

st.header('Diamond Luxury Tower Hotel')
page_awal = st.sidebar.selectbox("Room Hotel", ["Database Hotel","Additing Database"])

if page_awal == "Database Hotel":
    data = conn.query('SELECT * FROM hotel_room ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page_awal == "Additing Database":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO hotel_room (nama, gender, contact, series_room, other_needs, check_in, time_ci, check_out, time_co, payment, price) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':None, '6':'', '7':'', '8':'', '9':'', '10':'', '11':''})
            session.commit()

    data = conn.query('SELECT * FROM hotel_room ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_awal = result["nama"]
        gender_awal = result["gender"]
        contact_awal = result["contact"]
        room_awal = result["series_room"]
        other_awal = result["other_needs"]
        checkin_awal = result["check_in"]
        timeci_awal = result["time_ci"]
        checkout_awal = result["check_out"]
        timeco_awal = result["time_co"]
        payment_awal = result["payment"]
        price_awal = result["price"]

        with st.expander(f'a.n. {nama_awal}'):
            with st.form(f'data-{id}'):
                nama_akhir = st.text_input("nama", nama_awal)
                gender_akhir = st.selectbox("gender", list_gender, list_gender.index(gender_awal))
                contact_akhir = st.text_input("contact", contact_awal)
                room_akhir = st.multiselect("series_room", ['double bed', 'twin deluxe', 'premium class', 'business class', 'diamond class'], eval(room_awal))
                other_akhir = st.text_input("other_needs", other_awal)
                checkin_akhir = st.date_input("check_in", checkin_awal)
                timeci_akhir = st.time_input("time_ci", timeci_awal)
                checkout_akhir = st.date_input("check_out", checkout_awal)
                timeco_akhir = st.time_input("time_co", timeco_awal)
                payment_akhir = st.selectbox("payment", list_payment, list_payment.index(payment_awal))
                price_akhir = st.text_input("price", price_awal)

                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE hotel_room \
                                          SET nama=:1, gender=:2, contact=:3, series_room=:4, other_needs=:5 \
                                          check_in=:6, time_ci=:7, check_out=:8, time_co=:9, payment=:10, price=:11 \
                                          WHERE id=:12;')
                            session.execute(query, {'1':nama_akhir, '2':gender_akhir, '3':contact_akhir, '4':str(room_akhir), '5':other_akhir,'6':checkin_akhir, 
                                                    '7':timeci_akhir, '8':checkout_akhir, '9':timeco_akhir, '10':payment_akhir, '11':price_akhir, '12':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM hotel_room WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()

page_akhir = st.sidebar.selectbox("Restaurant Hotel", ["Database Restaurant","Additing Pelanggan"])

if page_akhir == "Database Restaurant":
    data = conn.query('SELECT * FROM hotel_restaurant ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page_akhir == "Additing Pelanggan":
    if st.button('Tambah Data'):
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