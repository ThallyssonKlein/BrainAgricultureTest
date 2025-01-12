CREATE TABLE farmers (
    id SERIAL PRIMARY KEY,
    document VARCHAR(14) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(2) NOT NULL
);

CREATE TABLE farms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    arable_area FLOAT NOT NULL,
    vegetation_area FLOAT NOT NULL,
    total_area FLOAT NOT NULL,
    farmer_id INTEGER NOT NULL REFERENCES farmers(id),
    city VARCHAR(255) NOT NULL,
    state VARCHAR(2) NOT NULL
);

CREATE TABLE cultures (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    farmer_id INTEGER NOT NULL REFERENCES farmers(id)
);

CREATE TABLE crops (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    culture_id INTEGER NOT NULL REFERENCES cultures(id),
    farm_id INTEGER NOT NULL REFERENCES farms(id)
);

INSERT INTO farmers (document, name, city, state)
VALUES 
('12345678901234', 'João da Silva', 'São Paulo', 'SP');

INSERT INTO farms (name, arable_area, vegetation_area, total_area, farmer_id, city, state)
VALUES
('Fazenda Sol Nascente', 100.5, 50.2, 150.7, 1, 'Campinas', 'SP'),
('Fazenda Estrela Guia', 200.0, 100.0, 300.0, 1, 'Sorocaba', 'SP'),
('Fazenda Boa Esperança', 50.0, 25.0, 75.0, 1, 'Piracicaba', 'SP');

INSERT INTO cultures (name, farmer_id)
VALUES
('Milho', 1),
('Soja', 1),
('Cana-de-Açúcar', 1);

INSERT INTO crops (date, culture_id, farm_id)
VALUES
('2025-01-15', 1, 1),
('2025-01-16', 2, 2),
('2025-01-17', 3, 3),
('2025-02-01', 1, 2),
('2025-02-10', 2, 3);
