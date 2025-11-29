-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. Attendance Table
create table if not exists attendance (
    id uuid default uuid_generate_v4() primary key,
    usage_date date,
    attendance integer
);

-- 2. Waiting Times Table
create table if not exists waiting_times (
    id uuid default uuid_generate_v4() primary key,
    work_date timestamp with time zone,
    wait_time_max integer,
    entity_description_short text,
    deb_time_hour integer,
    capacity integer
);

-- 3. Facilities Table
create table if not exists facilities (
    id uuid default uuid_generate_v4() primary key,
    facility_name text,
    type text,
    status text default 'Operational',
    location text
);

-- 4. Reviews Table
create table if not exists reviews (
    id uuid default uuid_generate_v4() primary key,
    review_text text,
    sentiment_score float,
    year_month text,
    rating integer,
    reviewer_location text
);

-- 5. Visitors Table (for System Health & Recommendations)
create table if not exists visitors (
    id uuid default uuid_generate_v4() primary key,
    age integer,
    weight_kg float,
    accompanied_with text,
    preference text,
    visit_date timestamp with time zone default now()
);

-- Insert some dummy data to prevent empty charts
insert into attendance (usage_date, attendance) values 
(current_date, 5000),
(current_date - interval '1 day', 4500),
(current_date - interval '2 day', 6000);

insert into waiting_times (work_date, wait_time_max, entity_description_short, deb_time_hour, capacity) values
(now(), 45, 'Roller Coaster', 14, 80),
(now() - interval '1 hour', 30, 'Ferris Wheel', 13, 60),
(now() - interval '2 hours', 15, 'Haunted House', 12, 40);

insert into facilities (facility_name, type, status) values
('Thunder Mountain', 'Ride', 'Operational'),
('Splash Log', 'Ride', 'Maintenance'),
('Main Food Court', 'Food', 'Operational');
