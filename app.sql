DROP TABLE IF EXISTS hotel_room;

CREATE TABLE hotel_room (
    id serial,
    nama text,
    gender text,
    contact text,
    series_room text,  
    other_needs text,
    check_in date,
    time_ci time,
    check_out date,
    time_co time,
    payment text,  
    price text  
);

insert into hotel_room  (nama, gender, contact, series_room, other_needs, check_in, time_ci, check_out, time_co, payment, price) 
values
	('Arindra Ningtiyas', 'male', '0812121', '["Twin Deluxe"]', 'Water', '2023-10-01', '13:00', '2023-10-02', '08:00', 'Tunai', '280000'),
	('Pahlawan Nur Ihzza', 'male', '0813876', '["Business Premium"]', 'Sandal', '2023-10-02', '14:00', '2023-10-04', '09:00', 'Transfer', '850000')
	;

DROP TABLE IF EXISTS hotel_restaurant;

CREATE TABLE hotel_restaurant (
    id serial,
    pelanggan text,
    makanan text,
    jumlah_makanan text,
    minuman text, 
    jumlah_minuman text,
    metode text,
    no_tempat text,
    total_harga text,
    pembayaran text
);

INSERT INTO hotel_restaurant (pelanggan, makanan, jumlah_makanan, minuman, jumlah_minuman, metode, no_tempat, total_harga, pembayaran) 
VALUES
    ('dr. Nurita', '["Mie Ayam Spesial"]', '2', '["Air Putih"]', '4', 'Diantar', 'Kamar 203', '60000', 'Tunai'),
    ('Aldenia Boo', '["Nasi Goreng Udang", "Mie Ayam Bakso"]', '1', '["Es Jeruk"]', '3', 'Ditunggu', 'Meja 8', '84000', 'ATM')
   	;