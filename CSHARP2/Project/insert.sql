-- Insert data into coworking_center
INSERT INTO coworking_center (name, description, latitude, longitude) VALUES
('TechHub Downtown', 'A premium coworking space in the city center.', 40.712776, -74.005974),
('Startup Haven', 'An innovative space for startups and entrepreneurs.', 34.052235, -118.243683),
('Freelancer Nest', 'Affordable and flexible working environment.', 51.507351, -0.127758),
('CodeWorks', 'Perfect for developers and remote teams.', 37.774929, -122.419418),
('Creative Loft', 'Designed for designers and artists.', 48.856613, 2.352222);

-- Insert data into workspace_status
INSERT INTO workspace_status (name, description) VALUES
('Available', 'The workspace is open for reservation.'),
('Reserved', 'The workspace is currently booked.'),
('Under Maintenance', 'The workspace is temporarily unavailable.'),
('Occupied', 'Currently in use but not reserved.');

-- Insert data into workspace
INSERT INTO workspace (name, description, coworking_center_id, status_id) VALUES
('Private Office A', 'A fully furnished private office.', 1, 1),
('Hot Desk 1', 'A flexible desk in an open space.', 1, 1),
('Conference Room X', 'A modern conference room with video conferencing.', 2, 2),
('Quiet Booth', 'A soundproof booth for deep work.', 3, 1),
('Lounge Area', 'Relaxed seating with great lighting.', 4, 3),
('Private Office B', 'Exclusive office for focused work.', 5, 1),
('Team Room', 'Perfect for small teams and collaboration.', 1, 2),
('Coworking Space', 'Shared space with ergonomic desks.', 2, 1);

-- Insert data into workspace_history
INSERT INTO workspace_history (workspace_id, status_id, created_at) VALUES
(1, 2, '2025-03-01 10:00:00'),
(1, 1, '2025-03-02 08:30:00'),
(2, 3, '2025-03-01 12:00:00'),
(3, 2, '2025-03-03 14:00:00'),
(4, 1, '2025-03-04 09:00:00'),
(5, 3, '2025-03-02 11:30:00');

-- Insert data into user_role
INSERT INTO user_role (name, description) VALUES
('Admin', 'Full access to the coworking management system.'),
('User', 'Can make reservations and view availability.'),
('Manager', 'Can manage coworking spaces and workspaces.');

-- Insert data into user
INSERT INTO "user" (email, password_hash, role_id) VALUES
('admin@cowork.com', 'hashedpassword123', 1),
('user1@example.com', 'hashedpassword456', 2),
('user2@example.com', 'hashedpassword789', 2),
('manager@cowork.com', 'hashedpassword321', 3);

-- Insert data into workspace_pricing
INSERT INTO workspace_pricing (workspace_id, price_per_hour, valid_from, valid_to) VALUES
(1, 20.00, '2025-03-01 00:00:00', NULL),
(2, 15.00, '2025-03-01 00:00:00', NULL),
(3, 50.00, '2025-03-01 00:00:00', NULL),
(4, 10.00, '2025-03-01 00:00:00', NULL),
(5, 25.00, '2025-03-01 00:00:00', NULL);

-- Insert data into reservation
INSERT INTO reservation (workspace_id, customer_email, start_time, end_time, price, pricing_id) VALUES
(1, 'user1@example.com', '2025-03-05 09:00:00', '2025-03-05 12:00:00', 60.00, 1),
(2, 'user2@example.com', '2025-03-06 10:00:00', '2025-03-06 13:00:00', 45.00, 2),
(3, 'user1@example.com', '2025-03-07 14:00:00', '2025-03-07 16:00:00', 100.00, 3),
(4, 'user2@example.com', '2025-03-08 08:00:00', '2025-03-08 09:30:00', 15.00, 4),
(5, 'admin@cowork.com', '2025-03-09 12:00:00', '2025-03-09 15:00:00', 75.00, 5);

