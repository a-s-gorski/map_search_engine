# Map Search Engine

A simple and efficient map search engine that allows users to search for locations, view maps, and get relevant information.

## Features

- Search for locations by name or coordinates.
- Display interactive maps with zoom and pan functionality.
- Retrieve detailed information about locations.
- Lightweight and user-friendly interface.
- Optimized for fast search results.
- Supports multiple map layers and themes.
- Mobile-friendly design for on-the-go usage.
- Easy integration with third-party APIs for extended functionality.

## Technologies Used

- **Backend**: Python, FastAPI
- **Frontend**: Steamlit
- **Database**: Postgres


## Running with Docker Compose

To simplify the setup and deployment, you can use Docker Compose to run the application.

### Prerequisites

- Install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

### Steps

1. Build and start the containers:
    ```bash
    docker-compose up --build
    ```
2. Access the application in your browser at `http://localhost:5000`.

### Configuration

- The `docker-compose.yml` file includes services for the application, database, and any other dependencies.
- Modify the `.env` file to configure environment variables as needed.

### Stopping the Application

To stop the containers, run:
```bash
docker-compose down
```

## License

This project is licensed under the [MIT License](LICENSE).