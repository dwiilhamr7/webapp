DROP TABLE IF EXISTS hotel_room;

CREATE TABLE hotel_room (
    id serial,
    nama text,
    gender text,
    contact text,
    series_room text[],  -- Menggunakan tipe array untuk series_room
    other_needs text,
    check_in text,
    time_ci text,
    check_out text,
    time_co text,
    payment text,  -- Menggunakan tipe data text untuk payment
    price text  -- Menggunakan tipe data numeric untuk price
);

INSERT INTO hotel_room (nama, gender, contact, series_room, other_needs, check_in, time_ci, check_out, time_co, payment, price) 
VALUES
    ('dr. Nurita', 'male', '0812121', ARRAY['twin deluxe'], 'water', '2023-10-01', '13:00', '2023-10-02', '08:00', 'Tunai', 280000),
    ('Aldenia Boo', 'female', '0812122018', ARRAY['twin deluxe'], 'water & sandals', '2023-10-02', '14:00', '2023-10-04', '08:00', 'Transfer', 1050000);
