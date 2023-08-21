echo 'Waiting for database...' ;
until PGPASSWORD="$POSTGRES_PASS" psql -h "localhost" -U "$POSTGRES_USER" -d "$POSTGRES_DBNAME" -c '\q'; \
do \
  >&2 echo 'PostgreSQL is unavailable - sleeping'; \
  sleep 1; \
done; \
>&2 echo 'PostgreSQL is up and running.'echo $POSTGRES_USER ; \
sleep 10 ; \
echo "timout finished" ; \
psql -U "$POSTGRES_USER" -d "$POSTGRES_DBNAME" -c "CREATE EXTENSION hstore;" ; \
osm2pgsql --cache 200000 -U "$POSTGRES_USER" -d "$POSTGRES_DBNAME" --style /configs/configuration.style  /data/opolskie-latest.osm --hstore ; \
echo "loaded postgis data" ; \
osmconvert /data/opolskie-latest.osm --drop-author --drop-version --out-osm -o=/data/opolskie_reduced.osm && \
echo "compressed data" ; \
osm2pgrouting -W "$POSTGRES_PASS" -U "$POSTGRES_USER" -d "$POSTGRES_DBNAME" -f /data/opolskie_reduced.osm --addnodes --attributes ; \
echo "loaded pgrouting data" ; \
for file in /sql_scripts/*.sql; do \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DBNAME" -f $file
done ;
