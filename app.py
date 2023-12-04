import streamlit as st
from sqlalchemy import text

list_room = ['', 'twin deluxe', 'double bed', 'premium intermediate', 'business premium', 'diamond class']
list_gender = ['', 'male', 'female']
list_payment = ['', 'ATM', 'Transfer', 'Tunai']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwiilhamr07:QBZxK7A6gYND@ep-hidden-unit-18107709.us-east-2.aws.neon.tech/web")

def main_home():
    st.title('Favorit Hotel in Jawa Timur')
    st.header('Drasri Beautiful Luxury Hotel')

with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS pelanggan (id serial, nama text, gender varchar, contact text, series_room varchar, other_needs text, \
                                                       check_in date, time_ci time, check_out date, time_co time, payment text, price text);')
    session.execute(query)

st.header('Reservation Drasri Beautifull Luxury Hotel')


page = st.sidebar.selectbox("Hotel Room", ["View Room","Edit Room"])

if page == "View Room":
    data = conn.query('SELECT * FROM pelanggan ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Room":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO pelanggan ("nama", "gender", "contact", "series_room", "other_needs", "check_in", "time_ci", "check_out", "time_co", "payment", "price") \
                         VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, ARRAY[:11]);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'', '5':None, '6':None, '7':'', '8':None, '9':'', '10':'', '11':['Rp']})
            session.commit()

    data = conn.query('SELECT * FROM pelanggan ORDER By id;', ttl="0")
    for _, result in data.iterrows():
        st.write(result) 
        id = result['id']
        nama_lama = result.loc["nama"]
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
            series_room_baru = st.selectbox("series_room", list_room, list_room.index(series_room_lama) if series_room_lama in list_room else 0) 
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
                            query = text('UPDATE pelanggan \
                                          SET nama=:1, gender=:2, contact=:3, series_room=:4, other_needs=:5 \
                                          check_in=:6, time_ci=:7, check_out=:8, time_co=:9, payment=:10, price=:11 \
                                          WHERE id=:12;')
                            session.execute(query, {'1':nama_baru, '2':gender_baru, '3':contact_baru, '4':series_room_baru, '5':other_needs_baru, 
                                                    '6':check_in_baru, '7':time_ci_baru, '8':check_out_baru, '9':time_co_baru, '10':payment_baru, '11':price_baru,
                                                    '12':id})
                            session.commit()
                            st.experimental_rerun()
                
            with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM pelanggan WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()

