SELECT name
FROM Songs
WHERE artist_id = (SELECT id FROM artists WHERE name=='Post Malone');