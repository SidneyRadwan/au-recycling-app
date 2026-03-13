-- H2 local seed data — matches V2__seed_data.sql structure
-- Tables are created by Hibernate DDL (ddl-auto: create-drop)

-- ── Materials ─────────────────────────────────────────────────────────────────

INSERT INTO materials (name, slug, category, description) VALUES
('Cardboard', 'cardboard', 'Paper & Cardboard', 'Corrugated boxes, cereal boxes, pizza boxes (clean)'),
('Paper', 'paper', 'Paper & Cardboard', 'Newspapers, magazines, office paper, junk mail'),
('Glass Bottles & Jars', 'glass-bottles-jars', 'Glass', 'Clear, brown, and green glass bottles and jars'),
('Plastic Bottles', 'plastic-bottles', 'Plastics', 'PET (#1) and HDPE (#2) plastic bottles'),
('Plastic Containers', 'plastic-containers', 'Plastics', 'Rigid plastic containers, tubs, and trays'),
('Steel Cans', 'steel-cans', 'Metals', 'Food tins, aerosol cans (empty)'),
('Aluminium Cans', 'aluminium-cans', 'Metals', 'Drink cans'),
('Aluminium Foil', 'aluminium-foil', 'Metals', 'Clean aluminium foil and trays, scrunched into a ball'),
('Food Waste', 'food-waste', 'Organic', 'Food scraps and leftovers'),
('Nappies', 'nappies', 'Sanitary', 'Disposable nappies and sanitary items'),
('Polystyrene', 'polystyrene', 'Plastics', 'Styrofoam cups, packaging, meat trays'),
('Soft Plastics', 'soft-plastics', 'Plastics', 'Plastic bags, cling wrap, chip packets, bread bags'),
('Broken Glass', 'broken-glass', 'Glass', 'Broken glass, crockery, ceramics, Pyrex'),
('Clothing & Textiles', 'clothing-textiles', 'Textiles', 'Old clothing and textiles (donate or special drop-off)'),
('Garden Organics', 'garden-organics', 'Organic', 'Grass clippings, leaves, branches, prunings'),
('Batteries', 'batteries', 'Hazardous', 'All battery types — never in general waste'),
('E-waste', 'e-waste', 'Electronics', 'Electronics, phones, computers, cables'),
('Paint', 'paint', 'Hazardous', 'Leftover paint'),
('Motor Oil', 'motor-oil', 'Hazardous', 'Used motor oil and lubricants'),
('Food Scraps', 'food-scraps', 'Organic', 'All food scraps including meat, dairy, and cooked food'),
('Pizza Box', 'pizza-box', 'Paper & Cardboard', 'Pizza boxes — clean ones go in recycling, greasy ones in general waste'),
('Coffee Cups', 'coffee-cups', 'Paper & Cardboard', 'Disposable coffee cups with plastic lining'),
('Milk Cartons', 'milk-cartons', 'Paper & Cardboard', 'Liquid paperboard cartons (Tetra Pak and similar)'),
('Shredded Paper', 'shredded-paper', 'Paper & Cardboard', 'Shredded paper — loose shredded paper can jam sorting machinery'),
('Plastic Bags', 'plastic-bags', 'Plastics', 'Shopping bags, bin liners, bread bags'),
('Bubble Wrap', 'bubble-wrap', 'Plastics', 'Bubble wrap and air cushion packaging');

-- ── Councils ──────────────────────────────────────────────────────────────────

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
('City of Adelaide', 'city-of-adelaide', 'SA', 'https://www.cityofadelaide.com.au', 'https://www.cityofadelaide.com.au/live-in-the-city/waste-recycling', 'City of Adelaide covers the Adelaide CBD and North Adelaide.');

-- ── Suburbs ───────────────────────────────────────────────────────────────────

INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Sydney', '2000', 'NSW', id FROM councils WHERE slug = 'city-of-sydney';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Pyrmont', '2009', 'NSW', id FROM councils WHERE slug = 'city-of-sydney';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Glebe', '2037', 'NSW', id FROM councils WHERE slug = 'city-of-sydney';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Surry Hills', '2010', 'NSW', id FROM councils WHERE slug = 'city-of-sydney';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Redfern', '2016', 'NSW', id FROM councils WHERE slug = 'city-of-sydney';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Newtown', '2042', 'NSW', id FROM councils WHERE slug = 'city-of-sydney';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Melbourne', '3000', 'VIC', id FROM councils WHERE slug = 'city-of-melbourne';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Carlton', '3053', 'VIC', id FROM councils WHERE slug = 'city-of-melbourne';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Fitzroy', '3065', 'VIC', id FROM councils WHERE slug = 'city-of-melbourne';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Richmond', '3121', 'VIC', id FROM councils WHERE slug = 'city-of-melbourne';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Brisbane City', '4000', 'QLD', id FROM councils WHERE slug = 'brisbane-city-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Fortitude Valley', '4006', 'QLD', id FROM councils WHERE slug = 'brisbane-city-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'West End', '4101', 'QLD', id FROM councils WHERE slug = 'brisbane-city-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Bondi Beach', '2026', 'NSW', id FROM councils WHERE slug = 'waverley-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Bondi Junction', '2022', 'NSW', id FROM councils WHERE slug = 'waverley-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Bronte', '2024', 'NSW', id FROM councils WHERE slug = 'waverley-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Marrickville', '2204', 'NSW', id FROM councils WHERE slug = 'inner-west-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Leichhardt', '2040', 'NSW', id FROM councils WHERE slug = 'inner-west-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Balmain', '2041', 'NSW', id FROM councils WHERE slug = 'inner-west-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'St Kilda', '3182', 'VIC', id FROM councils WHERE slug = 'port-phillip-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'South Melbourne', '3205', 'VIC', id FROM councils WHERE slug = 'port-phillip-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Brunswick', '3056', 'VIC', id FROM councils WHERE slug = 'moreland-city-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Coburg', '3058', 'VIC', id FROM councils WHERE slug = 'moreland-city-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Surfers Paradise', '4217', 'QLD', id FROM councils WHERE slug = 'gold-coast-city-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Broadbeach', '4218', 'QLD', id FROM councils WHERE slug = 'gold-coast-city-council';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Perth', '6000', 'WA', id FROM councils WHERE slug = 'city-of-perth';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Northbridge', '6003', 'WA', id FROM councils WHERE slug = 'city-of-perth';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'Adelaide', '5000', 'SA', id FROM councils WHERE slug = 'city-of-adelaide';
INSERT INTO suburbs (name, postcode, state, council_id) SELECT 'North Adelaide', '5006', 'SA', id FROM councils WHERE slug = 'city-of-adelaide';

-- ── Council Materials: City of Sydney ─────────────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Flatten boxes. Remove staples where possible.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Place loose in bin. No need to bag.', NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Rinse containers. Lids can be left on.', 'All colours accepted' FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Rinse containers. Leave lids on.', 'Eligible for Return and Earn 10c refund' FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Rinse clean. Must be larger than a credit card.', 'Numbers 1, 2, 3, 5 preferred' FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Rinse clean. Aerosols must be empty.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Rinse clean.', 'Eligible for Return and Earn 10c refund' FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Clean only. Scrunch into a ball larger than a fist.', NULL FROM materials WHERE slug = 'aluminium-foil';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'RECYCLING', 'Clean boxes go in recycling. Heavily soiled boxes in general waste.', 'Tear off clean top if bottom is greasy' FROM materials WHERE slug = 'pizza-box';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'GENERAL_WASTE', NULL, 'City of Sydney does not have a separate FOGO bin — food scraps go in general waste' FROM materials WHERE slug = 'food-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'GENERAL_WASTE', 'Wrap securely.', NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'GENERAL_WASTE', NULL, 'Cannot be recycled in kerbside bin' FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'GENERAL_WASTE', NULL, 'Most coffee cups cannot be recycled due to plastic lining. Use a reusable cup.' FROM materials WHERE slug = 'coffee-cups';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'GENERAL_WASTE', NULL, 'Loose shredded paper jams recycling machinery. Place in a sealed paper bag or general waste.' FROM materials WHERE slug = 'shredded-paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'GENERAL_WASTE', 'Wrap in newspaper and place in a sealed box labelled "broken glass".', 'Never loose in recycling bin' FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'SOFT_PLASTICS', 'Take to supermarket REDcycle drop-off point.', 'Do NOT put in yellow lid bin' FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'SOFT_PLASTICS', 'Take to supermarket REDcycle drop-off point.', 'Do NOT put in yellow lid bin' FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'GREEN_WASTE', 'Branches no longer than 1m and no thicker than 10cm.', 'Fortnightly collection' FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'SPECIAL_DROP_OFF', 'Take to a B-cycle collection point or council facility.', 'B-cycle drop-off at many retailers' FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'SPECIAL_DROP_OFF', 'Take to council e-waste drop-off or TechCollect point.', 'Free e-waste drop-off available' FROM materials WHERE slug = 'e-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-sydney'), id, 'SPECIAL_DROP_OFF', 'Take to Paintback collection point.', 'Many hardware stores accept paint' FROM materials WHERE slug = 'paint';

-- ── Council Materials: City of Melbourne ──────────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', 'Flatten boxes.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', NULL, NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', 'Rinse clean.', 'All colours accepted' FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', 'Rinse and replace lids.', NULL FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', 'Rinse clean.', 'Plastics 1-7 accepted' FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', 'Clean only. Scrunch into a ball.', NULL FROM materials WHERE slug = 'aluminium-foil';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'RECYCLING', 'Clean boxes only.', 'Greasy boxes in FOGO or general waste' FROM materials WHERE slug = 'pizza-box';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'GREEN_WASTE', 'Use compostable bags or newspaper to wrap.', 'FOGO bin — food AND garden organics accepted' FROM materials WHERE slug = 'food-scraps';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'GREEN_WASTE', 'All food scraps accepted including meat and dairy.', 'FOGO bin service' FROM materials WHERE slug = 'food-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'GREEN_WASTE', 'Branches up to 30cm long.', 'Combined with food in FOGO bin' FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'GENERAL_WASTE', NULL, 'Not accepted in recycling' FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'GENERAL_WASTE', 'Wrap in newspaper, label "broken glass".', 'Do not place loose in recycling' FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'GENERAL_WASTE', NULL, 'Plastic-lined cups cannot be recycled' FROM materials WHERE slug = 'coffee-cups';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'SPECIAL_DROP_OFF', 'Take to B-cycle collection point.', NULL FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-melbourne'), id, 'SPECIAL_DROP_OFF', 'Council provides free e-waste drop-off.', NULL FROM materials WHERE slug = 'e-waste';

-- ── Council Materials: Brisbane City Council ──────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'RECYCLING', 'Flatten and remove tape where possible.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'RECYCLING', NULL, NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'RECYCLING', 'Rinse and replace lids.', NULL FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'RECYCLING', 'Clean boxes in recycling. Greasy boxes in general waste.', NULL FROM materials WHERE slug = 'pizza-box';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'GENERAL_WASTE', NULL, 'Brisbane does not have a city-wide FOGO service' FROM materials WHERE slug = 'food-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'GENERAL_WASTE', 'Wrap securely and label.', NULL FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'coffee-cups';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'GREEN_WASTE', 'Branches up to 1.5m and 15cm diameter.', 'Fortnightly green bin service' FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'SOFT_PLASTICS', 'Take to supermarket soft plastics collection point.', 'Do NOT put in recycling bin' FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'SPECIAL_DROP_OFF', 'Take to B-cycle point — many retailers and council facilities.', NULL FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'brisbane-city-council'), id, 'SPECIAL_DROP_OFF', 'Council-run e-waste drop-off events and permanent facilities.', NULL FROM materials WHERE slug = 'e-waste';

-- ── Council Materials: Waverley Council ───────────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'RECYCLING', 'Flatten boxes.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'RECYCLING', NULL, NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'RECYCLING', 'Rinse clean.', 'Eligible for Return and Earn 10c refund' FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'RECYCLING', 'Rinse and replace lids.', 'Eligible for Return and Earn 10c refund' FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'RECYCLING', 'Rinse clean.', 'Eligible for Return and Earn 10c refund' FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'RECYCLING', 'Clean only. Scrunch into a ball.', NULL FROM materials WHERE slug = 'aluminium-foil';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'GREEN_WASTE', 'Branches no longer than 1m and no thicker than 10cm.', 'Fortnightly collection' FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'GENERAL_WASTE', NULL, 'No FOGO service — food goes in general waste' FROM materials WHERE slug = 'food-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'GENERAL_WASTE', 'Wrap securely before placing in bin.', NULL FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', 'Do NOT put in yellow lid bin' FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'SPECIAL_DROP_OFF', 'Take to B-cycle collection point.', NULL FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'SPECIAL_DROP_OFF', 'Free drop-off at council facilities or Officeworks.', NULL FROM materials WHERE slug = 'e-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'waverley-council'), id, 'SPECIAL_DROP_OFF', 'Take to Paintback collection point.', NULL FROM materials WHERE slug = 'paint';

-- ── Council Materials: Inner West Council ─────────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'RECYCLING', 'Flatten boxes.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'RECYCLING', NULL, NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'RECYCLING', 'Rinse clean.', 'Eligible for Return and Earn 10c refund' FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'RECYCLING', 'Rinse and replace lids.', 'Eligible for Return and Earn 10c refund' FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'RECYCLING', 'Clean only. Scrunch into a ball.', NULL FROM materials WHERE slug = 'aluminium-foil';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'GREEN_WASTE', 'Use compostable bags or newspaper to wrap food scraps.', 'Inner West has FOGO — food and garden organics together' FROM materials WHERE slug = 'food-scraps';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'GREEN_WASTE', 'Branches no longer than 30cm.', NULL FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'GENERAL_WASTE', 'Wrap securely before placing in bin.', NULL FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', 'Do NOT put in yellow lid bin' FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'SPECIAL_DROP_OFF', 'Take to B-cycle collection point.', NULL FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'inner-west-council'), id, 'SPECIAL_DROP_OFF', 'Free drop-off at council facilities.', NULL FROM materials WHERE slug = 'e-waste';

-- ── Council Materials: Port Phillip Council ───────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'RECYCLING', 'Flatten boxes.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'RECYCLING', NULL, NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'RECYCLING', 'Rinse clean.', 'All colours accepted' FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'RECYCLING', 'Rinse and replace lids.', NULL FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'GREEN_WASTE', 'Use compostable bags or newspaper to wrap.', 'FOGO service available' FROM materials WHERE slug = 'food-scraps';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'GREEN_WASTE', 'Branches up to 30cm long.', NULL FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'GENERAL_WASTE', 'Wrap in newspaper, label "broken glass".', NULL FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'SPECIAL_DROP_OFF', 'Take to B-cycle collection point.', NULL FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'SPECIAL_DROP_OFF', 'Free drop-off at council facilities.', NULL FROM materials WHERE slug = 'e-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'port-phillip-council'), id, 'SPECIAL_DROP_OFF', 'Take to Paintback collection point.', NULL FROM materials WHERE slug = 'paint';

-- ── Council Materials: Moreland City Council ──────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'RECYCLING', 'Flatten boxes.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'RECYCLING', NULL, NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'RECYCLING', 'Rinse clean.', 'All colours accepted' FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'RECYCLING', 'Rinse and replace lids.', NULL FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'GREEN_WASTE', 'Use compostable bags or newspaper to wrap.', 'FOGO service available' FROM materials WHERE slug = 'food-scraps';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'GREEN_WASTE', 'Branches up to 30cm long.', NULL FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'GENERAL_WASTE', 'Wrap in newspaper, label "broken glass".', NULL FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'SPECIAL_DROP_OFF', 'Take to B-cycle collection point.', NULL FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'moreland-city-council'), id, 'SPECIAL_DROP_OFF', 'Free drop-off at council facilities.', NULL FROM materials WHERE slug = 'e-waste';

-- ── Council Materials: Gold Coast City Council ────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'RECYCLING', 'Flatten boxes.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'RECYCLING', NULL, NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'RECYCLING', 'Rinse and replace lids.', NULL FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'GREEN_WASTE', 'Branches up to 1.5m and 15cm diameter.', 'Fortnightly green bin service' FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'GENERAL_WASTE', NULL, 'No city-wide FOGO service' FROM materials WHERE slug = 'food-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'GENERAL_WASTE', 'Wrap securely and label.', NULL FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', 'Do NOT put in recycling bin' FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'SPECIAL_DROP_OFF', 'Take to B-cycle collection point.', NULL FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'gold-coast-city-council'), id, 'SPECIAL_DROP_OFF', 'Council-run e-waste drop-off facilities.', NULL FROM materials WHERE slug = 'e-waste';

-- ── Council Materials: City of Perth ──────────────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'RECYCLING', 'Flatten boxes.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'RECYCLING', NULL, NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'RECYCLING', 'Rinse clean.', 'All colours accepted' FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'RECYCLING', 'Rinse and replace lids.', NULL FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'GREEN_WASTE', 'Branches up to 1m long.', 'Fortnightly collection' FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'food-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'GENERAL_WASTE', 'Wrap securely and label.', NULL FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', 'Do NOT put in yellow lid bin' FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'SPECIAL_DROP_OFF', 'Take to B-cycle collection point or council facility.', NULL FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'SPECIAL_DROP_OFF', 'Free drop-off at council facilities or Officeworks.', NULL FROM materials WHERE slug = 'e-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-perth'), id, 'SPECIAL_DROP_OFF', 'Take to Paintback collection point.', NULL FROM materials WHERE slug = 'paint';

-- ── Council Materials: City of Adelaide ───────────────────────────────────────

INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'RECYCLING', 'Flatten boxes.', NULL FROM materials WHERE slug = 'cardboard';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'RECYCLING', NULL, NULL FROM materials WHERE slug = 'paper';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'RECYCLING', 'Rinse clean.', 'All colours accepted' FROM materials WHERE slug = 'glass-bottles-jars';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'RECYCLING', 'Rinse and replace lids.', NULL FROM materials WHERE slug = 'plastic-bottles';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'plastic-containers';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'RECYCLING', 'Rinse clean.', NULL FROM materials WHERE slug = 'steel-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'RECYCLING', 'Rinse clean.', 'Eligible for 10c container deposit refund' FROM materials WHERE slug = 'aluminium-cans';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'RECYCLING', 'Rinse and flatten.', NULL FROM materials WHERE slug = 'milk-cartons';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'GREEN_WASTE', 'Branches up to 1m long.', 'Fortnightly collection' FROM materials WHERE slug = 'garden-organics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'food-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'polystyrene';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'GENERAL_WASTE', 'Wrap securely and label.', NULL FROM materials WHERE slug = 'broken-glass';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'GENERAL_WASTE', NULL, NULL FROM materials WHERE slug = 'nappies';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', 'Do NOT put in yellow lid bin' FROM materials WHERE slug = 'soft-plastics';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'SOFT_PLASTICS', 'Take to supermarket collection point.', NULL FROM materials WHERE slug = 'plastic-bags';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'SPECIAL_DROP_OFF', 'Take to B-cycle collection point or council facility.', NULL FROM materials WHERE slug = 'batteries';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'SPECIAL_DROP_OFF', 'Free drop-off at council facilities or Officeworks.', NULL FROM materials WHERE slug = 'e-waste';
INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes) SELECT (SELECT id FROM councils WHERE slug = 'city-of-adelaide'), id, 'SPECIAL_DROP_OFF', 'Take to Paintback collection point.', NULL FROM materials WHERE slug = 'paint';
