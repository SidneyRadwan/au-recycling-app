-- Seed data: Materials (common recyclable/waste items)
INSERT INTO materials (name, slug, category, description) VALUES
-- Recycling
('Cardboard', 'cardboard', 'Paper & Cardboard', 'Corrugated boxes, cereal boxes, pizza boxes (clean)'),
('Paper', 'paper', 'Paper & Cardboard', 'Newspapers, magazines, office paper, junk mail'),
('Glass Bottles & Jars', 'glass-bottles-jars', 'Glass', 'Clear, brown, and green glass bottles and jars'),
('Plastic Bottles', 'plastic-bottles', 'Plastics', 'PET (#1) and HDPE (#2) plastic bottles'),
('Plastic Containers', 'plastic-containers', 'Plastics', 'Rigid plastic containers, tubs, and trays'),
('Steel Cans', 'steel-cans', 'Metals', 'Food tins, aerosol cans (empty)'),
('Aluminium Cans', 'aluminium-cans', 'Metals', 'Drink cans'),
('Aluminium Foil', 'aluminium-foil', 'Metals', 'Clean aluminium foil and trays, scrunched into a ball'),
-- General waste
('Food Waste', 'food-waste', 'Organic', 'Food scraps and leftovers'),
('Nappies', 'nappies', 'Sanitary', 'Disposable nappies and sanitary items'),
('Polystyrene', 'polystyrene', 'Plastics', 'Styrofoam cups, packaging, meat trays'),
('Soft Plastics', 'soft-plastics', 'Plastics', 'Plastic bags, cling wrap, chip packets, bread bags'),
('Broken Glass', 'broken-glass', 'Glass', 'Broken glass, crockery, ceramics, Pyrex'),
('Clothing & Textiles', 'clothing-textiles', 'Textiles', 'Old clothing and textiles (donate or special drop-off)'),
-- Green waste
('Garden Organics', 'garden-organics', 'Organic', 'Grass clippings, leaves, branches, prunings'),
-- Special categories
('Batteries', 'batteries', 'Hazardous', 'All battery types — never in general waste'),
('E-waste', 'e-waste', 'Electronics', 'Electronics, phones, computers, cables'),
('Paint', 'paint', 'Hazardous', 'Leftover paint'),
('Motor Oil', 'motor-oil', 'Hazardous', 'Used motor oil and lubricants'),
-- FOGO
('Food Scraps', 'food-scraps', 'Organic', 'All food scraps including meat, dairy, and cooked food'),
-- Tricky items
('Pizza Box', 'pizza-box', 'Paper & Cardboard', 'Pizza boxes — clean ones go in recycling, greasy ones in general waste'),
('Coffee Cups', 'coffee-cups', 'Paper & Cardboard', 'Disposable coffee cups with plastic lining'),
('Milk Cartons', 'milk-cartons', 'Paper & Cardboard', 'Liquid paperboard cartons (Tetra Pak and similar)'),
('Shredded Paper', 'shredded-paper', 'Paper & Cardboard', 'Shredded paper — loose shredded paper can jam sorting machinery'),
('Plastic Bags', 'plastic-bags', 'Plastics', 'Shopping bags, bin liners, bread bags'),
('Bubble Wrap', 'bubble-wrap', 'Plastics', 'Bubble wrap and air cushion packaging')
ON CONFLICT (slug) DO NOTHING;
