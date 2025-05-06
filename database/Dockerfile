FROM kartoza/postgis

# Set environment variables
ENV POSTGRES_USER=root \
    POSTGRES_PASS=password \
    PGPASSWORD=password \
    POSTGRES_DBNAME=postgis \
    POSTGRES_MULTIPLE_EXTENSIONS=postgis,pgrouting

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-15-pgrouting \
        osm2pgsql \
        osm2pgrouting \
        osmosis \
        osmctools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy necessary files
COPY sql_scripts/ /sql_scripts/
COPY data/ /data/
COPY migrate-spatial-data.sh /scripts/migrate-spatial-data.sh
COPY configuration.style /configs/configuration.style
COPY mapconfig.xml /configs/mapconfig.xml

# Ensure scripts have execution permissions
RUN chmod +x /scripts/migrate-spatial-data.sh

# Expose PostgreSQL port
EXPOSE 5432

# Set entrypoint and default command
ENTRYPOINT ["/bin/bash", "-c", "/scripts/migrate-spatial-data.sh & /scripts/docker-entrypoint.sh"]
CMD ["postgres", "-c", "max_connections=300", \
     "-c", "log_statement=all", \
     "-c", "log_destination=stderr", \
     "-c", "logging_collector=on", \
     "-c", "log_directory=/var/log/postgresql", \
     "-c", "log_filename=postgresql-%Y-%m-%d_%H%M%S.log", \
     "-c", "log_truncate_on_rotation=on", \
     "-c", "log_rotation_age=1440", \
     "-c", "log_rotation_size=0"]