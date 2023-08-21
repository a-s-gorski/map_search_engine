DROP FUNCTION IF EXISTS get_closest_way(lon double precision, lat double precision);
CREATE OR REPLACE FUNCTION get_closest_way(lon double precision, lat double precision)
RETURNS BIGINT AS $$
DECLARE
    osm_id_result BIGINT;
BEGIN
    SELECT osm_id into osm_id_result
        FROM ways
        ORDER BY st_distance(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(ways.x1, ways.y1), 4326))
        LIMIT 1;
    RETURN osm_id_result;
END;
$$ LANGUAGE plpgsql;