import streamlit as st
from sqlalchemy import text

list_room = ['', 'twin deluxe', 'double bed', 'premium intermediate', 'business premium', 'diamond class']
list_gender = ['', 'male', 'female']
list_payment = ['', 'ATM', 'Transfer', 'Tunai']
list_metode = ['','Diantar', 'Ditunggu']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwiilhamr07:QBZxK7A6gYND@ep-hidden-unit-18107709.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query_room = text('CREATE TABLE IF NOT EXISTS hotel_room (id serial, nama text, gender varchar, contact text, series_room varchar, other_needs text, \
                                                       check_in date, time_ci time, check_out date, time_co time, payment text, price text);')
    query_restaurant = text('CREATE TABLE IF NOT EXISTS hotel_restaurant (id serial, pelanggan text, makanan varchar, jumlah_makanan integer, minuman varchar, \
                                                       jumlah_minuman integer, metode text, no_tempat text, total_harga integer, pembayaran text);')
    session.execute(query_room)
    session.execute(query_restaurant)

def home():
    st.title('DIAMOND LUXURY TOWER HOTEL')
    st.header('DATABASE INTERNAL STAFF')

    image_path = "https://www.theluxevoyager.com/wp-content/uploads/2018/02/Four-Seasons-Hotel-Jakarta-pool.jpg"
    st.image(image_path, caption='Warning! Database hanya diakses oleh karyawan/staff hotel')

    st.subheader("Pelayanan :")
    st.markdown("- Penyimpanan Data Room Hotel")
    st.markdown("- Penyimpanan Data Restaurant")
    st.markdown("- Penambahan Data")
    st.markdown("- Visualisasi Data")

def room_hotel():
    st.header('Reservation Room Hotel Diamond Luxury Tower Hotel')
    page = st.sidebar.selectbox("Room Hotel", ['View Data Room Hotel', 'Additing Data Room Hotel'])

    if page == "View Data Room Hotel":
        data = conn.query('Select * FROM hotel_room ORDER BY id;', ttl="0").set_index('id')
        st.dataframe(data)
    
    if page == "Additing Data Room Hotel":
        if st.button('Tambah Data'):
            with conn.session as session:
                query_room = text('INSERT INTO hotel_room ("nama", "gender", "contact", "series_room", "other_needs", "check_in", "time_ci", "check_out", "time_co", "payment", "price") \
                        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);')
                session.execute(query_room, {'1':'', '2':'', '3':'', '4':'', '5':None, '6':'', '7':'', '8':'', '9':'', '10':'', '11':0})
                session.commit()
        
    data = conn.query('SELECT * FROM hotel_room ORDER By id;', ttl="0")
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

    with st.expander(f'a.n. {nama_lama}'):
        with st.form(f'data-{id}'):
            nama_baru = st.text_input("nama", nama_lama)
            gender_baru = st.selectbox("gender", list_gender, list_gender.index(gender_lama))
            contact_baru = st.text_input("contact", contact_lama)
            series_room_baru = st.selectbox("series_room", list_room, list_room.index(series_room_lama)) 
            other_needs_baru = st.text_input("other_needs", other_needs_lama)
            check_in_baru = st.date_input("check_in", check_in_lama)
            time_ci_baru = st.time_input("time_ci", time_ci_lama)
            check_out_baru = st.date_input("check_out", check_out_lama)
            time_co_baru = st.time_input("time_co", time_co_lama)
            payment_baru = st.selectbox("payment", list_payment, list_payment.index(payment_lama))
            price_baru = st.text_input("price", price_lama)
                
            col1, col2 = st.columns([1, 6])

            with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query_room = text('UPDATE hotel_room \
                                          SET nama=:1, gender=:2, contact=:3, series_room=:4, other_needs=:5 \
                                          check_in=:6, time_ci=:7, check_out=:8, time_co=:9, payment=:10, price=:11 \
                                          WHERE id=:12;')
                            session.execute(query_room, {'1':nama_baru, '2':gender_baru, '3':contact_baru, '4':series_room_baru, '5':other_needs_baru, 
                                                    '6':check_in_baru, '7':time_ci_baru, '8':check_out_baru, '9':time_co_baru, '10':payment_baru, '11':price_baru,
                                                    '12':id})
                            session.commit()
                            st.experimental_rerun()

            with col2:
                    if st.form_submit_button('DELETE'):
                        query_room = text(f'DELETE FROM hotel_room WHERE id=:1;')
                        session.execute(query_room, {'1':id})
                        session.commit()
                        st.experimental_rerun()

def restaurant_hotel():
    st.header('Reservation Restaurant Diamond Luxury Tower Hotel')

    page = st.sidebar.selectbox("Restaurant Hotel", ['View Data Restaurant', 'Additing Data Restaurant'])

    if page == "View Data Restaurant":
        data = conn.query('Select * FROM hotel_restaurant ORDER BY id;', ttl="0").set_index('id')
        st.dataframe(data)
    
    if page == "Additing Data Restaurant":
        if st.button('Tambah Data'):
            with conn.session as session:
                query_restaurant = text('INSERT INTO hotel_restaurant ("pelanggan", "makanan", "jumlah_makanan", "minuman", "jumlah_minuman", "metode", "no_tempat", "total_harga", "pembayaran") \
                        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9);')
                session.execute(query_restaurant, {'1':'', '2':None, '3':0, '4':None, '5':0, '6':'', '7':'', '8':0, '9':''})
                session.commit()
        
    data = conn.query('SELECT * FROM hotel_restaurant ORDER By id;', ttl="0")
    for _, result in data.iterrows():
        id = result['id']
        pelanggan_lama = result["pelanggan"]
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
                            query_restaurant = text('UPDATE hotel_restaurant \
                                          SET pelanggan=:1, makanan=:2, jumlah_makanan=:3, minuman=:4, jumlah_minuman=:5 \
                                          metode=:6, no_tempat=:7, total_harga=:8, pembayaran=:9, \
                                          WHERE id=:10;')
                            session.execute(query_restaurant, {'1':pelanggan_baru, '2':makanan_baru, '3':jumlah_makanan_baru, '4':minuman_baru, '5':jumlah_minuman_baru, 
                                                    '6':metode_baru, '7':no_tempat_baru, '8':total_harga_baru, '9':pembayaran_baru, 
                                                    '10':id})
                            session.commit()
                            st.experimental_rerun()

            with col2:
                    if st.form_submit_button('DELETE'):
                        query_restaurant = text(f'DELETE FROM hotel_restaurant WHERE id=:1;')
                        session.execute(query_restaurant, {'1':id})
                        session.commit()
                        st.experimental_rerun()

if st.sidebar.checkbox("Room Hotel"):
    room_hotel()
if st.sidebar.checkbox("Restaurant Hotel"):
    restaurant_hotel()
else:
    home()