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