-- Database schema for Chikukwa Bus Booking System

-- Create bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    ticket_id VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(255),
    departure VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    time VARCHAR(20) NOT NULL,
    seat INTEGER NOT NULL,
    fare DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'confirmed',
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster ticket lookups
CREATE INDEX IF NOT EXISTS idx_ticket_id ON bookings(ticket_id);
CREATE INDEX IF NOT EXISTS idx_status ON bookings(status);
CREATE INDEX IF NOT EXISTS idx_date ON bookings(date);

-- Create routes table
CREATE TABLE IF NOT EXISTS routes (
    id SERIAL PRIMARY KEY,
    route_name VARCHAR(200) UNIQUE NOT NULL,
    fare DECIMAL(10, 2) NOT NULL,
    schedule VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create bus_stops table
CREATE TABLE IF NOT EXISTS bus_stops (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) UNIQUE NOT NULL,
    stops TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create system_config table
CREATE TABLE IF NOT EXISTS system_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default routes
INSERT INTO routes (route_name, fare, schedule) VALUES
    ('Bulawayo to Gweru', 5, '08:00 AM'),
    ('Gweru to Bulawayo', 5, '02:00 PM'),
    ('Bulawayo to Kwekwe', 7, '09:00 AM'),
    ('Kwekwe to Bulawayo', 7, '03:30 PM'),
    ('Bulawayo to Kadoma', 8, '10:00 AM'),
    ('Kadoma to Bulawayo', 8, '04:30 PM'),
    ('Bulawayo to Chegutu', 10, '11:00 AM'),
    ('Chegutu to Bulawayo', 10, '05:00 PM'),
    ('Bulawayo to Norton', 13, '12:00 PM'),
    ('Norton to Bulawayo', 13, '06:00 PM'),
    ('Bulawayo to Harare', 15, '12:00 PM'),
    ('Harare to Bulawayo', 15, '06:00 PM'),
    ('Gweru to Kwekwe', 3, '09:00 AM'),
    ('Kwekwe to Gweru', 3, '03:00 PM'),
    ('Gweru to Kadoma', 4, '09:30 AM'),
    ('Kadoma to Gweru', 4, '02:30 PM'),
    ('Gweru to Chegutu', 5, '10:15 AM'),
    ('Chegutu to Gweru', 5, '03:15 PM'),
    ('Gweru to Norton', 6, '11:00 AM'),
    ('Norton to Gweru', 6, '04:00 PM'),
    ('Gweru to Harare', 7, '11:30 AM'),
    ('Harare to Gweru', 7, '05:00 PM'),
    ('Kwekwe to Kadoma', 2, '10:00 AM'),
    ('Kadoma to Kwekwe', 2, '04:00 PM'),
    ('Kwekwe to Chegutu', 6, '10:45 AM'),
    ('Chegutu to Kwekwe', 6, '04:15 PM'),
    ('Kwekwe to Norton', 9, '11:30 AM'),
    ('Norton to Kwekwe', 9, '05:15 PM'),
    ('Kwekwe to Harare', 10, '12:15 PM'),
    ('Harare to Kwekwe', 10, '06:15 PM'),
    ('Kadoma to Chegutu', 4, '10:30 AM'),
    ('Chegutu to Kadoma', 4, '04:45 PM'),
    ('Kadoma to Norton', 5, '11:00 AM'),
    ('Norton to Kadoma', 5, '05:00 PM'),
    ('Kadoma to Harare', 6, '11:30 AM'),
    ('Harare to Kadoma', 6, '05:30 PM'),
    ('Chegutu to Norton', 1, '11:45 AM'),
    ('Norton to Chegutu', 1, '05:45 PM'),
    ('Chegutu to Harare', 3, '12:15 PM'),
    ('Harare to Chegutu', 3, '06:15 PM'),
    ('Norton to Harare', 2, '12:30 PM'),
    ('Harare to Norton', 2, '06:30 PM')
ON CONFLICT (route_name) DO NOTHING;

-- Insert default bus stops
INSERT INTO bus_stops (city, stops) VALUES
    ('Bulawayo', 'City Hall, Renkini Bus Terminus, and National Railways of Zimbabwe Station.'),
    ('Gweru', 'Main Street, City Centre, and Railway Station.'),
    ('Kwekwe', 'City Centre, Kwekwe Mall, and Railway Station.'),
    ('Kadoma', 'City Centre, Kadoma Mall, and Railway Station.'),
    ('Chegutu', 'City Centre, Chegutu Mall, and Railway Station.'),
    ('Norton', 'Main Street, Town Centre, and near the Post Office.'),
    ('Harare', 'City Centre, Avondale, and Mbare Musika Bus Terminus.')
ON CONFLICT (city) DO NOTHING;

-- Insert system configuration
INSERT INTO system_config (config_key, config_value) VALUES
    ('total_seats', '50'),
    ('company_name', 'Chikukwa Bus Services'),
    ('contact_phone', '+263777189947'),
    ('contact_email', 'support@chikukwabus.com')
ON CONFLICT (config_key) DO NOTHING;
