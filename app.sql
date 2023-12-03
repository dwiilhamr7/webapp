DROP TABLE IF EXISTS pelanggan;

CREATE TABLE pelanggan (
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
    price numeric  -- Menggunakan tipe data numeric untuk price
);

INSERT INTO pelanggan (nama, gender, contact, series_room, other_needs, check_in, time_ci, check_out, time_co, payment, price) 
VALUES
    ('dr. Nurita', 'male', '0812121', ARRAY['twin deluxe'], 'water', '2023-10-01', '13:00', '2023-10-02', '08:00', 'Tunai', 280000),
    ('Aldenia Boo', 'female', '0812122018', ARRAY['luxury class'], 'water & sandals', '2023-10-02', '14:00', '2023-10-04', '08:00', 'Transfer', 1050000);
