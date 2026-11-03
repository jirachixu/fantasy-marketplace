CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    gold_balance INT NOT NULL DEFAULT 1000 CHECK (gold_balance >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS materials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS user_materials (
    user_id INT REFERENCES users(id) ON DELETE CASCADE, -- if a user is deleted, their materials are also deleted
    material_id INT REFERENCES materials(id) ON DELETE CASCADE,
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    PRIMARY KEY (user_id, material_id)
);

CREATE TABLE IF NOT EXISTS item_types (
    id VARCHAR(50) PRIMARY KEY,
    type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    owner_id INT REFERENCES users(id) ON DELETE CASCADE,
    item_type VARCHAR(50) REFERENCES item_types(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    base VARCHAR(50) NOT NULL,
    level VARCHAR(50) NOT NULL,
    prefix VARCHAR(50),
    suffix VARCHAR(50),
    is_listed BOOLEAN NOT NULL DEFAULT FALSE,
    is_equipped BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS weapons (
    item_id INT PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
    physical_damage FLOAT NOT NULL CHECK (physical_damage >= 0),
    magic_damage FLOAT NOT NULL CHECK (magic_damage >= 0),
    speed FLOAT NOT NULL,
    range FLOAT NOT NULL,
    fire_damage FLOAT NOT NULL DEFAULT 0,
    ice_damage FLOAT NOT NULL DEFAULT 0,
    lightning_damage FLOAT NOT NULL DEFAULT 0,
    void_damage FLOAT NOT NULL DEFAULT 0,
    arcane_damage FLOAT NOT NULL DEFAULT 0,
    true_damage FLOAT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS armor (
    item_id INT PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
    defense FLOAT NOT NULL,
    movement_speed FLOAT NOT NULL,
    magic_resist FLOAT NOT NULL,
    fire_resist FLOAT NOT NULL DEFAULT 1,
    ice_resist FLOAT NOT NULL DEFAULT 1,
    lightning_resist FLOAT NOT NULL DEFAULT 1,
    void_resist FLOAT NOT NULL DEFAULT 1,
    arcane_resist FLOAT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS item_tags (
    item_id INT REFERENCES items(id) ON DELETE CASCADE,
    tag VARCHAR(50) NOT NULL,
    source VARCHAR(50) NOT NULL CHECK (source IN ('base', 'level', 'prefix', 'suffix', 'rune')),
    PRIMARY KEY (item_id, tag, source)
);

CREATE TABLE IF NOT EXISTS runes (
    id SERIAL PRIMARY KEY,
    owner_id INT REFERENCES users(id) ON DELETE CASCADE,
    rune_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    stat_to_modify VARCHAR(50) NOT NULL,
    multiplier FLOAT NOT NULL,
    is_slotted BOOLEAN NOT NULL DEFAULT FALSE,
    apply_to VARCHAR(50) NOT NULL CHECK (apply_to IN ('weapon', 'armor')),
    is_elemental BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS item_sockets (
    item_id INT REFERENCES items(id) ON DELETE CASCADE,
    socket_index INT NOT NULL,
    rune_id INT UNIQUE REFERENCES runes(id) ON DELETE SET NULL,
    PRIMARY KEY (item_id, socket_index)
);

CREATE TABLE IF NOT EXISTS crafting_recipes (
    id SERIAL PRIMARY KEY,
    result_item_type VARCHAR(50) REFERENCES item_types(id) ON DELETE CASCADE,
    result_base VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS crafting_recipe_materials (
    recipe_id INT REFERENCES crafting_recipes(id) ON DELETE CASCADE,
    material_id INT REFERENCES materials(id) ON DELETE CASCADE,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (recipe_id, material_id)
);

CREATE TABLE IF NOT EXISTS marketplace_listings (
    id SERIAL PRIMARY KEY,
    item_id INT REFERENCES items(id) ON DELETE CASCADE,
    seller_id INT REFERENCES users(id) ON DELETE CASCADE,
    price INT NOT NULL CHECK (price > 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('active', 'sold', 'cancelled')),
    listed_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS marketplace_transactions (
    id SERIAL PRIMARY KEY,
    listing_id INT REFERENCES marketplace_listings(id) ON DELETE SET NULL,
    buyer_id INT REFERENCES users(id) ON DELETE CASCADE,
    seller_id INT REFERENCES users(id) ON DELETE SET NULL,
    item_id INT REFERENCES items(id) ON DELETE SET NULL,
    transaction_price INT NOT NULL CHECK (transaction_price > 0),
    transaction_time TIMESTAMP NOT NULL DEFAULT NOW()
);