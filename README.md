This is a boilerplate code for starting off fastapi app server implemented with DDD project structure.  

## Getting Started

To get started with this project, follow the steps below:

1. Clone the repository:

    ```bash
    git clone https://github.com/shivama205/ai-service.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure the environment variables:

    Create a `.env` file in the root directory and add the following variables:

    ```plaintext
    SECRET_KEY=your-secret-key
    ```

4. Start the server:

    ```bash
    uvicorn main:app --reload --port=8080 --host=0.0.0.0
    ```

5. Open your browser and navigate to `http://localhost:8000` to access the app.

6. Use Docker (optional):

    To run the application using Docker, follow these steps:

    - Build the Docker image:

        ```bash
        docker build -t ai-service .
        ```

    - Run the Docker container:

        ```bash
        docker run -p 8080:8080 ai-service
        ```

    - Open your browser and navigate to `http://localhost:8080` to access the app.

## Project Structure

The project follows the Domain-Driven Design (DDD) architecture, with the following structure:

```
├── api
│   ├── routers
│   ├── container.py
├── infrastructure
│   ├── databases
│   ├── repositories
├── models
│   ├── constants
│   ├── schemas
└── main.py
└── middleware.py
└── logger.py
└── README.md
└── Dockerfile
└── docker-compose.yml
```

This structure organizes the codebase into different modules and layers, promoting separation of concerns and maintainability. Here's a brief overview of each directory:

- `api`: Contains the API routers and the dependency container module.
- `infrastructure`: Includes modules for handling databases and repositories.
- `models`: Contains constants and schemas used in the application.
- `main.py`: The entry point of the FastAPI application.
- `middleware.py`: Middleware functions for request processing.
- `logger.py`: Logging configuration for the application.
- `README.md`: The project's README file.
- `Dockerfile`: Configuration for building a Docker image.
- `docker-compose.yml`: Docker Compose configuration for running the application.

Feel free to explore and modify the project structure to fit your specific requirements.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

