drop table if exists schedule;
create table schedule (
	id serial,
	customer text,
	gender text,
	contact text,
	series_room text,
	other_needs text,
	check_in text,
	time_ci text,
	check_out text,
	time_co text,
	payment time,
	price date
);

insert into schedule (customer, gender, contact, series_room, other_needs, check_in, time_ci, check_out, time_co, payment, price) 
values
	('dr. Nurita', 'male', '["twin deluxe"]', 'water', '13:00', '2023-10-01', '08:00', '2023-10-02', 'Tunai', 'Rp. 280.000'),
	('Aldenia Boo', 'female', '["luxury class"]', 'water & sandals', '14:00', '2023-10-02', '08:00', '2023-10-04', 'Transfer', 'Rp. 1.050.000')
	;