# Stockwatch

REST API built with Django 5.2 and DRF, featuring tiered account access, stock watchlist management, and JWT-secured authentication.

## Quick Start

Create a .env file in the root directory and paste your configuration, include the following:

DB_NAME=stockdb
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=db
DB_PORT=5432
DEBUG=1
SECRET_KEY=my-secret-key

The SECRET_KEY provided in the .env sample is for development only. In a production environment, ensure you use a strong, unique key and set DEBUG=0.


## Makefile for ease of commands:

* make up        # Build and start containers (Postgres & Django)
* make migrate   # Run database migrations
* make superuser # Create your admin account


## API:

* API Root: http://127.0.0.1:8000/api/v1/
* Swagger Docs: http://127.0.0.1:8000/api/v1/docs/ 

## Pending Features
Due to the assignment's time constraints, the following features are planned for the next phase:
* **Real-time Data Integration:** Connecting to live stock feeds (e.g., Alpha Vantage or YFinance).
* **Distributed Task Queue:** Implementing Celery/Redis for background analytics processing.
* **Enhanced Caching:** Using Redis to cache frequent market data queries.