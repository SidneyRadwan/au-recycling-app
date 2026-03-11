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

-- Seed data: Councils
INSERT INTO councils (name, slug, state, website, recycling_info_url, description) VALUES
('City of Sydney', 'city-of-sydney', 'NSW', 'https://www.cityofsydney.nsw.gov.au', 'https://www.cityofsydney.nsw.gov.au/recycling-and-waste', 'The City of Sydney Council covers the Sydney CBD and surrounding inner suburbs.'),
('City of Melbourne', 'city-of-melbourne', 'VIC', 'https://www.melbourne.vic.gov.au', 'https://www.melbourne.vic.gov.au/residents/waste-recycling', 'City of Melbourne serves the CBD and surrounding inner suburbs including Carlton, Fitzroy, and Richmond.'),
('Brisbane City Council', 'brisbane-city-council', 'QLD', 'https://www.brisbane.qld.gov.au', 'https://www.brisbane.qld.gov.au/clean-and-green/rubbish-and-recycling', 'Brisbane City Council is Australia''s largest local government, covering all of Brisbane.'),
('Waverley Council', 'waverley-council', 'NSW', 'https://www.waverley.nsw.gov.au', 'https://www.waverley.nsw.gov.au/council/waste-recycling', 'Waverley Council covers the eastern suburbs including Bondi Beach, Bondi Junction, and Tamarama.'),
('Inner West Council', 'inner-west-council', 'NSW', 'https://www.innerwest.nsw.gov.au', 'https://www.innerwest.nsw.gov.au/live/waste-and-recycling', 'Inner West Council covers suburbs including Ashfield, Balmain, Leichhardt, Marrickville, and Newtown.'),
('Port Phillip Council', 'port-phillip-council', 'VIC', 'https://www.portphillip.vic.gov.au', 'https://www.portphillip.vic.gov.au/environment/recycling-waste', 'City of Port Phillip covers St Kilda, South Melbourne, Port Melbourne, and Albert Park.'),
('Moreland City Council', 'moreland-city-council', 'VIC', 'https://www.moreland.vic.gov.au', 'https://www.moreland.vic.gov.au/environment/waste', 'Moreland City Council (now Merri-bek) covers Brunswick, Coburg, and Glenroy.'),
('Gold Coast City Council', 'gold-coast-city-council', 'QLD', 'https://www.goldcoast.qld.gov.au', 'https://www.goldcoast.qld.gov.au/services/waste-recycling', 'Gold Coast City Council covers the entire Gold Coast region including Surfers Paradise and Coolangatta.'),
('City of Perth', 'city-of-perth', 'WA', 'https://www.perth.wa.gov.au', 'https://www.perth.wa.gov.au/residents/waste-recycling', 'City of Perth covers the Perth CBD and immediate surrounds.'),
('City of Adelaide', 'city-of-adelaide', 'SA', 'https://www.cityofadelaide.com.au', 'https://www.cityofadelaide.com.au/live-in-the-city/waste-recycling', 'City of Adelaide covers the Adelaide CBD and North Adelaide.')
ON CONFLICT (slug) DO NOTHING;

-- Suburbs for City of Sydney
INSERT INTO suburbs (name, postcode, state, council_id)
SELECT s.name, s.postcode, 'NSW', c.id
FROM (VALUES
    ('Sydney', '2000'),
    ('Pyrmont', '2009'),
    ('Glebe', '2037'),
    ('Surry Hills', '2010'),
    ('Redfern', '2016'),
    ('Chippendale', '2008'),
    ('Darlinghurst', '2010'),
    ('Paddington', '2021'),
    ('Waterloo', '2017'),
    ('Zetland', '2017'),
    ('Alexandria', '2015'),
    ('Erskineville', '2043'),
    ('Newtown', '2042'),
    ('Forest Lodge', '2037')
) AS s(name, postcode)
CROSS JOIN (SELECT id FROM councils WHERE slug = 'city-of-sydney') c
ON CONFLICT DO NOTHING;

-- Suburbs for City of Melbourne
INSERT INTO suburbs (name, postcode, state, council_id)
SELECT s.name, s.postcode, 'VIC', c.id
FROM (VALUES
    ('Melbourne', '3000'),
    ('Carlton', '3053'),
    ('Fitzroy', '3065'),
    ('Richmond', '3121'),
    ('South Yarra', '3141'),
    ('St Kilda', '3182'),
    ('Port Melbourne', '3207'),
    ('Docklands', '3008'),
    ('Southbank', '3006'),
    ('East Melbourne', '3002')
) AS s(name, postcode)
CROSS JOIN (SELECT id FROM councils WHERE slug = 'city-of-melbourne') c
ON CONFLICT DO NOTHING;

-- Suburbs for Brisbane
INSERT INTO suburbs (name, postcode, state, council_id)
SELECT s.name, s.postcode, 'QLD', c.id
FROM (VALUES
    ('Brisbane City', '4000'),
    ('Fortitude Valley', '4006'),
    ('New Farm', '4005'),
    ('Teneriffe', '4005'),
    ('Paddington', '4064'),
    ('Red Hill', '4059'),
    ('Ashgrove', '4060'),
    ('Toowong', '4066'),
    ('West End', '4101'),
    ('South Brisbane', '4101'),
    ('Woolloongabba', '4102'),
    ('Spring Hill', '4000')
) AS s(name, postcode)
CROSS JOIN (SELECT id FROM councils WHERE slug = 'brisbane-city-council') c
ON CONFLICT DO NOTHING;

-- Suburbs for Waverley
INSERT INTO suburbs (name, postcode, state, council_id)
SELECT s.name, s.postcode, 'NSW', c.id
FROM (VALUES
    ('Bondi', '2026'),
    ('Bondi Beach', '2026'),
    ('Bondi Junction', '2022'),
    ('Bronte', '2024'),
    ('Clovelly', '2031'),
    ('Tamarama', '2026'),
    ('Waverley', '2024'),
    ('Dover Heights', '2030'),
    ('Rose Bay', '2029'),
    ('Vaucluse', '2030')
) AS s(name, postcode)
CROSS JOIN (SELECT id FROM councils WHERE slug = 'waverley-council') c
ON CONFLICT DO NOTHING;

-- Suburbs for Inner West
INSERT INTO suburbs (name, postcode, state, council_id)
SELECT s.name, s.postcode, 'NSW', c.id
FROM (VALUES
    ('Newtown', '2042'),
    ('Marrickville', '2204'),
    ('Leichhardt', '2040'),
    ('Balmain', '2041'),
    ('Rozelle', '2039'),
    ('Annandale', '2038'),
    ('Ashfield', '2131'),
    ('Dulwich Hill', '2203'),
    ('Haberfield', '2045'),
    ('Summer Hill', '2130'),
    ('Stanmore', '2048'),
    ('Petersham', '2049'),
    ('Tempe', '2044'),
    ('St Peters', '2044')
) AS s(name, postcode)
CROSS JOIN (SELECT id FROM councils WHERE slug = 'inner-west-council') c
ON CONFLICT DO NOTHING;

-- Council Materials for City of Sydney
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes)
SELECT c.id, m.id, cm.bin_type, cm.instructions, cm.notes
FROM (VALUES
    ('cardboard', 'RECYCLING', 'Flatten boxes. Remove staples where possible.', null),
    ('paper', 'RECYCLING', 'Place loose in bin. No need to bag.', null),
    ('glass-bottles-jars', 'RECYCLING', 'Rinse containers. Lids can be left on.', 'All colours accepted'),
    ('plastic-bottles', 'RECYCLING', 'Rinse containers. Leave lids on.', 'Eligible for Return and Earn 10c refund'),
    ('plastic-containers', 'RECYCLING', 'Rinse clean. Must be larger than a credit card.', 'Numbers 1, 2, 3, 5 preferred'),
    ('steel-cans', 'RECYCLING', 'Rinse clean. Aerosols must be empty.', null),
    ('aluminium-cans', 'RECYCLING', 'Rinse clean.', 'Eligible for Return and Earn 10c refund'),
    ('aluminium-foil', 'RECYCLING', 'Clean only. Scrunch into a ball larger than a fist.', null),
    ('milk-cartons', 'RECYCLING', 'Rinse and flatten.', null),
    ('food-waste', 'GENERAL_WASTE', null, 'City of Sydney does not have a separate FOGO bin - food scraps go in general waste'),
    ('nappies', 'GENERAL_WASTE', 'Wrap securely.', null),
    ('polystyrene', 'GENERAL_WASTE', null, 'Cannot be recycled in kerbside bin'),
    ('soft-plastics', 'SOFT_PLASTICS', 'Take to supermarket REDcycle drop-off point.', 'Do NOT put in yellow lid bin'),
    ('plastic-bags', 'SOFT_PLASTICS', 'Take to supermarket REDcycle drop-off point.', 'Do NOT put in yellow lid bin'),
    ('garden-organics', 'GREEN_WASTE', 'Branches no longer than 1m and no thicker than 10cm.', 'Fortnightly collection'),
    ('batteries', 'SPECIAL_DROP_OFF', 'Take to a B-cycle collection point or council facility.', 'B-cycle drop-off at many retailers'),
    ('e-waste', 'SPECIAL_DROP_OFF', 'Take to council e-waste drop-off or TechCollect point.', 'Free e-waste drop-off available'),
    ('paint', 'SPECIAL_DROP_OFF', 'Take to Paintback collection point.', 'Many hardware stores accept paint'),
    ('pizza-box', 'RECYCLING', 'Clean boxes go in recycling. Heavily soiled boxes in general waste.', 'Tear off clean top if bottom is greasy'),
    ('coffee-cups', 'GENERAL_WASTE', null, 'Most coffee cups cannot be recycled due to plastic lining. Use a reusable cup.'),
    ('shredded-paper', 'GENERAL_WASTE', null, 'Loose shredded paper jams recycling machinery. Place in a sealed paper bag or general waste.'),
    ('broken-glass', 'GENERAL_WASTE', 'Wrap in newspaper and place in a sealed box labelled "broken glass".', 'Never loose in recycling bin')
) AS cm(material_slug, bin_type, instructions, notes)
CROSS JOIN (SELECT id FROM councils WHERE slug = 'city-of-sydney') c
JOIN materials m ON m.slug = cm.material_slug
ON CONFLICT (council_id, material_id) DO NOTHING;

-- Council Materials for City of Melbourne (has FOGO)
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes)
SELECT c.id, m.id, cm.bin_type, cm.instructions, cm.notes
FROM (VALUES
    ('cardboard', 'RECYCLING', 'Flatten boxes.', null),
    ('paper', 'RECYCLING', null, null),
    ('glass-bottles-jars', 'RECYCLING', 'Rinse clean.', 'All colours accepted'),
    ('plastic-bottles', 'RECYCLING', 'Rinse and replace lids.', null),
    ('plastic-containers', 'RECYCLING', 'Rinse clean.', 'Plastics 1-7 accepted'),
    ('steel-cans', 'RECYCLING', 'Rinse clean.', null),
    ('aluminium-cans', 'RECYCLING', 'Rinse clean.', null),
    ('aluminium-foil', 'RECYCLING', 'Clean only. Scrunch into a ball.', null),
    ('milk-cartons', 'RECYCLING', 'Rinse and flatten.', null),
    ('food-scraps', 'GREEN_WASTE', 'Use compostable bags or newspaper to wrap.', 'FOGO bin — food AND garden organics accepted'),
    ('food-waste', 'GREEN_WASTE', 'All food scraps accepted including meat and dairy.', 'FOGO bin service'),
    ('garden-organics', 'GREEN_WASTE', 'Branches up to 30cm long.', 'Combined with food in FOGO bin'),
    ('nappies', 'GENERAL_WASTE', null, null),
    ('polystyrene', 'GENERAL_WASTE', null, 'Not accepted in recycling'),
    ('soft-plastics', 'SOFT_PLASTICS', 'Take to supermarket collection point.', null),
    ('plastic-bags', 'SOFT_PLASTICS', 'Take to supermarket collection point.', null),
    ('batteries', 'SPECIAL_DROP_OFF', 'Take to B-cycle collection point.', null),
    ('e-waste', 'SPECIAL_DROP_OFF', 'Council provides free e-waste drop-off.', null),
    ('broken-glass', 'GENERAL_WASTE', 'Wrap in newspaper, label "broken glass".', 'Do not place loose in recycling'),
    ('coffee-cups', 'GENERAL_WASTE', null, 'Plastic-lined cups cannot be recycled'),
    ('pizza-box', 'RECYCLING', 'Clean boxes only.', 'Greasy boxes in FOGO or general waste')
) AS cm(material_slug, bin_type, instructions, notes)
CROSS JOIN (SELECT id FROM councils WHERE slug = 'city-of-melbourne') c
JOIN materials m ON m.slug = cm.material_slug
ON CONFLICT (council_id, material_id) DO NOTHING;

-- Council Materials for Brisbane City Council
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes)
SELECT c.id, m.id, cm.bin_type, cm.instructions, cm.notes
FROM (VALUES
    ('cardboard', 'RECYCLING', 'Flatten and remove tape where possible.', null),
    ('paper', 'RECYCLING', null, null),
    ('glass-bottles-jars', 'RECYCLING', 'Rinse clean.', null),
    ('plastic-bottles', 'RECYCLING', 'Rinse and replace lids.', null),
    ('plastic-containers', 'RECYCLING', 'Rinse clean.', null),
    ('steel-cans', 'RECYCLING', 'Rinse clean.', null),
    ('aluminium-cans', 'RECYCLING', 'Rinse clean.', null),
    ('milk-cartons', 'RECYCLING', 'Rinse and flatten.', null),
    ('food-waste', 'GENERAL_WASTE', null, 'Brisbane does not have a city-wide FOGO service'),
    ('garden-organics', 'GREEN_WASTE', 'Branches up to 1.5m and 15cm diameter.', 'Fortnightly green bin service'),
    ('nappies', 'GENERAL_WASTE', null, null),
    ('polystyrene', 'GENERAL_WASTE', null, null),
    ('soft-plastics', 'SOFT_PLASTICS', 'Take to supermarket soft plastics collection point.', 'Do NOT put in recycling bin'),
    ('plastic-bags', 'SOFT_PLASTICS', 'Take to supermarket collection point.', null),
    ('batteries', 'SPECIAL_DROP_OFF', 'Take to B-cycle point — many retailers and council facilities.', null),
    ('e-waste', 'SPECIAL_DROP_OFF', 'Council-run e-waste drop-off events and permanent facilities.', null),
    ('broken-glass', 'GENERAL_WASTE', 'Wrap securely and label.', null),
    ('coffee-cups', 'GENERAL_WASTE', null, null),
    ('pizza-box', 'RECYCLING', 'Clean boxes in recycling. Greasy boxes in general waste.', null)
) AS cm(material_slug, bin_type, instructions, notes)
CROSS JOIN (SELECT id FROM councils WHERE slug = 'brisbane-city-council') c
JOIN materials m ON m.slug = cm.material_slug
ON CONFLICT (council_id, material_id) DO NOTHING;
