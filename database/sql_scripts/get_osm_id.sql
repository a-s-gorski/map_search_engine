DROP FUNCTION IF EXISTS get_osm_id(city TEXT, street TEXT, house_number TEXT);
CREATE OR REPLACE FUNCTION get_osm_id(city TEXT, street TEXT, house_number TEXT)
RETURNS BIGINT AS $$
DECLARE
  osm_id_result BIGINT;
BEGIN
    SELECT osm_id INTO osm_id_result
    FROM planet_osm_point
    WHERE lower("addr:city") ilike lower(city)
    AND lower("addr:street") ilike lower(street)
    AND lower("addr:housenumber") ilike lower(house_number)
    LIMIT 1;

    IF osm_id_result IS NULL THEN
        SELECT osm_id INTO osm_id_result
        FROM planet_osm_point
        WHERE lower("addr:city") ilike lower(city)
        AND lower("addr:street") ilike lower(street)
        LIMIT 1;
    END IF;

    IF osm_id_result IS NULL THEN
        SELECT osm_id INTO osm_id_result
        FROM planet_osm_point
        WHERE lower("addr:city") ilike lower(city)
        LIMIT 1;
    END IF;

    RETURN osm_id_result;
END;
$$ LANGUAGE plpgsql;

