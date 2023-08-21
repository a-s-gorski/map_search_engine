DROP FUNCTION IF EXISTS get_long_lat(osm_id_param BIGINT);
CREATE OR REPLACE FUNCTION get_long_lat(osm_id_param BIGINT)
RETURNS TABLE (long double precision, lat double precision) AS $$
BEGIN
    RETURN QUERY SELECT ST_X(ST_Transform(way, 4326)), ST_Y(ST_Transform(way, 4326))
        FROM planet_osm_point
        WHERE planet_osm_point.osm_id = osm_id_param
        LIMIT 1;
END;
$$ LANGUAGE plpgsql;