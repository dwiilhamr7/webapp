import streamlit as st
from sqlalchemy import text

list_room = ['', 'twin_deluxe', 'double_bed', 'premium_intermediate', 'business_premium', 'diamond_class', 'Paket_Request']
list_gender = ['', 'male', 'female']
list_payment = ['', 'ATM', 'Transfer', 'Tunai']
list_metode = ['','Diantar', 'Ditunggu']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwiilhamr07:QBZxK7A6gYND@ep-hidden-unit-18107709.us-east-2.aws.neon.tech/web")

st.header('Diamond Luxury Tower Hotel')
page_awal = st.sidebar.selectbox("Room Hotel", ["Database Hotel","Additing Database"])

with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS hotel_room (id serial, nama text, gender char(25), contact text, series_hotel_room text, other_needs text, \
                                                       check_in date, time_ci text, check_out date, time_co text, payment text, price text);')
    session.execute(query)


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
                room_akhir = st.selectbox("series_room", list_room, list_room.index(room_awal))
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
