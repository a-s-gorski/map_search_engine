DROP FUNCTION IF EXISTS get_optimal_start_end_vid(start_osm_id bigint, end_osm_id bigint);

CREATE OR REPLACE FUNCTION get_optimal_start_end_vid(start_osm_id bigint, end_osm_id bigint, velocity float)
RETURNS TABLE (start_vid_output bigint, end_vid_output bigint)
AS $$
BEGIN
    SELECT subquery.start_vid, subquery.end_vid
    FROM (
        SELECT start_vid, end_vid, sum(cost) AS total_cost
        FROM pgr_dijkstra(
            'SELECT gid as id, source, target, length / LEAST(' || velocity ||  ', maxspeed_forward) as cost FROM ways',
            ARRAY(SELECT gid FROM ways WHERE osm_id = start_osm_id),
            ARRAY(SELECT gid FROM ways WHERE osm_id = end_osm_id),
            directed => true
        ) AS path
        GROUP BY start_vid, end_vid
        ORDER BY total_cost
        LIMIT 1
    ) AS subquery
    INTO start_vid_output, end_vid_output;

    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;