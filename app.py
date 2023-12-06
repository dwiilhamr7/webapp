import streamlit as st
from sqlalchemy import text

list_room = ['', 'Twin Deluxe', 'Double Bed', 'Family Class', 'Business Premium', 'Diamond Class', 'VVIP Class']
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

    st.subheader("Anggota Kelompok :")
    st.markdown("- Melynda Isaura (2043221015)")
    st.markdown("- Hellen Aldenia R. (2043221046)")
    st.markdown("- Dwi Ilham Ramadhany (2043221054)")
    st.markdown("- Avika Niswata M. (2043221060)")
    st.markdown("- M. Rafli Nugrahasyach (2043221085)")

def room_hotel():
    
    st.header('Diamond Luxury Tower Hotel')
    page_awal = st.sidebar.selectbox("Room Hotel", ["Database Hotel","Adding Database"])

    with conn.session as session:
        query = text('CREATE TABLE IF NOT EXISTS hotel_room (id serial, nama text, gender char(25), contact text, series_hotel_room text, other_needs text, \
                                                            check_in date, time_ci text, check_out date, time_co text, payment text, price text);')
        session.execute(query)

    if page_awal == "Database Hotel":
        data = conn.query('SELECT * FROM hotel_room ORDER By id;', ttl="0").set_index('id')
        st.dataframe(data)

    if page_awal == "Adding Database":
        if st.button('Tambah Data'):
            with conn.session as session:
                query = text('INSERT INTO hotel_room (nama, gender, contact, series_room, other_needs, check_in, time_ci, check_out, time_co, payment, price) \
                                VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);')
                session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':'', '6':None, '7':None, '8':None, '9':None, '10':'', '11':'0'})
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
                    room_akhir = st.multiselect("series_room", ['Twin Deluxe', 'Double Bed', 'Family Class', 'Business Premium', 'Diamond Class', 'VVIP Class'], eval(room_awal))
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
                                            SET nama=:1, gender=:2, contact=:3, series_room=:4, other_needs=:5, \
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

def restaurant_hotel():
    
    st.header('Diamond Luxury Tower Hotel')
    page_akhir = st.sidebar.selectbox("Restaurant Hotel", ["Database Restaurant","Adding Pelanggan"])

    with conn.session as session:
        query = text('CREATE TABLE IF NOT EXISTS hotel_restaurant (id serial, pelanggan text, makanan text, jumlah_makanan text, minuman text, \
                                                        jumlah_minuman text, metode text, no_tempat text, total_harga text, pembayaran text);')
        session.execute(query)

    if page_akhir == "Database Restaurant":
        data = conn.query('SELECT * FROM hotel_restaurant ORDER By id;', ttl="0").set_index('id')
        st.dataframe(data)

    if page_akhir == "Adding Pelanggan":
        if st.button('Adding'):
            with conn.session as session:
                    query_restaurant = text('INSERT INTO hotel_restaurant ("pelanggan", "makanan", "jumlah_makanan", "minuman", "jumlah_minuman", "metode", "no_tempat", "total_harga", "pembayaran") \
                            VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9);')
                    session.execute(query_restaurant, {'1':'', '2':'[]', '3':'0', '4':'[]', '5':'0', '6':'', '7':'', '8':'0', '9':''})
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

            with st.expander(f'a.n. {pelanggan_awal}'):
                with st.form(f'data-{id}'):
                    pelanggan_akhir = st.text_input("nama", pelanggan_awal)
                    makanan_akhir = st.multiselect("makanan", ['Mie Ayam Bakso', 'Mie Ayam Spesial', 'Nasi Goreng Udang', 'Nasi Goreng Daging', 'Bakso Spesial', 'Steak With Omelette', 'Roti Panggang', 'Pisang Goreng CokJu', 'Rice Box Rendang',], eval(makanan_awal))
                    jumlah_makanan_akhir = st.text_input("jumlah_makanan", jumlah_makanan_awal)
                    minuman_akhir = st.multiselect("minuman", ['Air Putih' 'Es Teh', 'Es Jeruk', 'Es Campur', 'STMJ', 'Ice Cream', 'Soda Angkasa', 'Kopi Hitam', 'Juice', 'Avocado Syrup'], eval(minuman_awal)) 
                    jumlah_minuman_akhir = st.text_input("jumlah_minuman", jumlah_minuman_awal)
                    metode_akhir = st.selectbox("metode", list_metode, list_metode.index(metode_awal))
                    no_tempat_akhir = st.text_input("no_tempat", no_tempat_awal)
                    total_harga_akhir = st.text_input("total_harga", total_harga_awal)
                    pembayaran_akhir = st.selectbox("pembayaran", list_payment, list_payment.index(pembayaran_awal))

                    col1, col2 = st.columns([1, 6])

                    with col1:
                        if st.form_submit_button('UPDATE'):
                            with conn.session as session:
                                query = text('UPDATE hotel_restaurant \
                                            SET pelanggan=:1, makanan=:2, jumlah_makanan=:3, minuman=:4, jumlah_minuman=:5, \
                                            metode=:6, no_tempat=:7, total_harga=:8, pembayaran=:9 \
                                            WHERE id=:10;')
                                session.execute(query, {'1':pelanggan_akhir, '2':str(makanan_akhir), '3':jumlah_makanan_akhir, '4':str(minuman_akhir), '5':jumlah_minuman_akhir, 
                                                        '6':metode_akhir, '7':no_tempat_akhir, '8':total_harga_akhir, '9':pembayaran_akhir, '10':id})
                                session.commit()
                                st.experimental_rerun()
                    
                    with col2:
                        if st.form_submit_button('DELETE'):
                            query = text(f'DELETE FROM hotel_restaurant WHERE id=:1;')
                            session.execute(query, {'1':id})
                            session.commit()
                            st.experimental_rerun()
   
def visualisasi_data():
    st.header('Visualisasi Database Diamond Luxury Tower Hotel')
    page_visul = st.sidebar.selectbox("Visualisasi", ["Data Hotel","Data Restaurant"])

    if page_visul == "Data Hotel":
        data = conn.query('SELECT * FROM hotel_restaurant ORDER By id;', ttl="0").set_index('id')
        st.dataframe(data)

    if page_visul == "Data Restaurant":
        data = conn.query('SELECT * FROM hotel_restaurant ORDER By id;', ttl="0").set_index('id')
        st.dataframe(data)


if st.sidebar.checkbox("Room Hotel"):
        room_hotel()
if st.sidebar.checkbox("Restaurant Hotel"):
        restaurant_hotel()
if st.sidebar.checkbox("Visualisasi"):
        visualisasi_data()
else:
    home()