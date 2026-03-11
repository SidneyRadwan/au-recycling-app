CREATE TABLE councils (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    state VARCHAR(10) NOT NULL,
    website VARCHAR(500),
    recycling_info_url VARCHAR(500),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE suburbs (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    state VARCHAR(10) NOT NULL,
    council_id BIGINT REFERENCES councils(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE materials (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100),
    description TEXT,
    common_aliases TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE council_materials (
    id BIGSERIAL PRIMARY KEY,
    council_id BIGINT REFERENCES councils(id),
    material_id BIGINT REFERENCES materials(id),
    bin_type VARCHAR(50) NOT NULL,
    instructions TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(council_id, material_id)
);

CREATE INDEX idx_councils_slug ON councils(slug);
CREATE INDEX idx_councils_state ON councils(state);
CREATE INDEX idx_suburbs_name ON suburbs(name);
CREATE INDEX idx_suburbs_postcode ON suburbs(postcode);
CREATE INDEX idx_suburbs_council_id ON suburbs(council_id);
CREATE INDEX idx_materials_slug ON materials(slug);
CREATE INDEX idx_materials_category ON materials(category);
CREATE INDEX idx_council_materials_council ON council_materials(council_id);
CREATE INDEX idx_council_materials_material ON council_materials(material_id);
