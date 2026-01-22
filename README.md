# Address Book API

A modern FastAPI-based address book application with geolocation capabilities, following clean architecture principles with Route → Service → Repository pattern.

## Architecture

The application follows a clean layered architecture:

```
┌─────────────────┐
│   Routes Layer  │  ← HTTP handlers, request/response
└─────────────────┘
        │
        ▼
┌─────────────────┐
│ Service Layer  │  ← Business logic, validation
└─────────────────┘
        │
        ▼
┌─────────────────┐
│Repository Layer│  ← Data access, database operations
└─────────────────┘
```

## Project Structure

```
app/
├── main.py                    # FastAPI application entry point
├── core/                      # Core application functionality
│   ├── settings.py            # Application configuration
│   └── logging.py            # Logging configuration
├── api/                       # API layer (Routes)
│   └── v1/
│       ├── api.py             # API router aggregation
│       └── endpoints/
│           └── address.py     # Address endpoints
├── models/                    # Database models
│   └── address_model.py     # Address data model
├── schemas/                   # Pydantic schemas
│   └── address_schema.py    # Request/response schemas
├── services/                  # Business logic layer
│   ├── address_service.py   # Address business logic
│   └── location_service.py  # Geolocation utilities
├── repositories/              # Data access layer
│   └── address_repository.py # Database operations
└── db/                       # Database configuration
    └── base.py             # Database session management
```

## Features

- ** Geolocation Support**: Automatic geocoding of addresses
- ** Radius Search**: Find addresses within specified distance
- ** Clean Architecture**: Route → Service → Repository pattern
- ** Modern Python**: SQLModel, Pydantic, FastAPI
- ** OpenStreetMap Integration**: Nominatim geocoding service

## Installation

### Prerequisites
- Python 3.8+
- Git

### Quick Start

1. **Clone the repository**:
```bash
git clone <repository-url>
cd Address_book_api
```

2. **Install uv**:
```bash
pip install uv
```

3. **Install dependencies**:
```bash
uv sync
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start the application**:
```bash
uv run uvicorn app.main:app --reload
```

### Alternative Setup (Using pip directly)

1. **Clone and navigate**:
```bash
git clone <repository-url>
cd Address_book_api
```

2. **Install dependencies**:
```bash
pip install fastapi uvicorn sqlmodel pydantic pydantic-settings requests
```

3. **Set environment variables**:
```bash
export APP_NAME="Address Book API"
export DATABASE_URL="sqlite:///./address_book.db"
export GEOCODE_URL="https://nominatim.openstreetmap.org/search"
```

4. **Run the server**:
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Running the Application

Once installed, you can start the application in several ways:

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (if available)
```bash
docker build -t address-book-api .
docker run -p 8000:8000 address-book-api
```

### Access Points
- **API Base URL**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Address Management

| Method | Endpoint | Description |
|---------|-----------|-------------|
| `POST` | `/api/v1/addresses/` | Create new address |
| `GET` | `/api/v1/addresses/{address_id}` | Get address by ID |
| `PUT` | `/api/v1/addresses/{address_id}` | Update address |
| `DELETE` | `/api/v1/addresses/{address_id}` | Delete address |
| `GET` | `/api/v1/addresses/search/` | Search addresses by radius |

### Request/Response Examples

#### Create Address
**Request:**
```bash
POST /api/v1/addresses/
Content-Type: application/json

{
    "building": "Times Square",
    "area": "Broadway & 7th Ave",
    "city": "New York",
    "country": "USA"
}
```

**Response:**
```json
{
    "id": "d1a5f3c2-1b2c-4e9f-9a33-8a2d9f3a1c11",
    "building": "Times Square",
    "area": "Broadway & 7th Ave",
    "city": "New York",
    "country": "USA",
    "latitude": 40.7580,
    "longitude": -73.9855,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}
```

#### Get Address
**Request:**
```bash
GET /api/v1/addresses/d1a5f3c2-1b2c-4e9f-9a33-8a2d9f3a1c11
```

**Response:**
```json
{
    "id": "d1a5f3c2-1b2c-4e9f-9a33-8a2d9f3a1c11",
    "building": "Times Square",
    "area": "Broadway & 7th Ave",
    "city": "New York",
    "country": "USA",
    "latitude": 40.7580,
    "longitude": -73.9855,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}
```

#### Update Address
**Request:**
```bash
PUT /api/v1/addresses/d1a5f3c2-1b2c-4e9f-9a33-8a2d9f3a1c11
Content-Type: application/json
{
    "area": "7th Avenue & Broadway, Midtown"
}
```

**Response:**
```json
{
    "id": "d1a5f3c2-1b2c-4e9f-9a33-8a2d9f3a1c11",
    "building": "Times Square",
    "area": "7th Avenue & Broadway, Midtown",
    "city": "New York",
    "country": "USA",
    "latitude": 40.7580,
    "longitude": -73.9855,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T01:00:00"
}
```

#### Delete Address
**Request:**
```bash
DELETE /api/v1/addresses/d1a5f3c2-1b2c-4e9f-9a33-8a2d9f3a1c11
```

**Response:** `204 No Content`

#### Search Addresses by Radius
**Request:**
```bash
GET /api/v1/addresses/search/?lat=40.7580&lon=-73.9855&radius_km=5
```

**Response:**
```json
[
    {
        "id": "a1b2c3d4-1111-2222-3333-444455556666",
        "building": "Bryant Park",
        "area": "6th Ave & W 42nd St",
        "city": "New York",
        "country": "USA",
        "latitude": 40.7536,
        "longitude": -73.9832,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": "b2c3d4e5-7777-8888-9999-000011112222",
        "building": "Rockefeller Center",
        "area": "45 Rockefeller Plaza",
        "city": "New York",
        "country": "USA",
        "latitude": 40.7587,
        "longitude": -73.9787,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": "c3d4e5f6-aaaa-bbbb-cccc-ddddeeeeffff",
        "building": "Grand Central Terminal",
        "area": "89 E 42nd St",
        "city": "New York",
        "country": "USA",
        "latitude": 40.7527,
        "longitude": -73.9772,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
]
```

#### Search by Address String
**Request:**
```bash
GET /api/v1/addresses/search/?address="Central Park, New York"&radius_km=2
```

**Response:**
```json
[
    {
        "id": "d1a5f3c2-1b2c-4e9f-9a33-8a2d9f3a1c11",
        "building": "Times Square",
        "area": "Broadway & 7th Ave",
        "city": "New York",
        "country": "USA",
        "latitude": 40.7829,
        "longitude": -73.9654,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
]
```

## Configuration

Environment variables in `.env`:

```bash
# Application
APP_NAME="Address Book API"
DEBUG=false

# Database
DATABASE_URL="sqlite:///./address_book.db"

# Geocoding
GEOCODE_URL="https://nominatim.openstreetmap.org/search"
```

## Testing

Run the test suite:
```bash
pytest
```

## Data Models

### Address Model
```python
{
    {
        "id": "d1a5f3c2-1b2c-4e9f-9a33-8a2d9f3a1c11",
        "building": "Times Square",
        "area": "Broadway & 7th Ave",
        "city": "New York",
        "country": "USA",
        "latitude": 40.7829,
        "longitude": -73.9654,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
}
```

## Request/Response Flow

1. **Request** → Route layer receives HTTP request
2. **Validation** → Pydantic schemas validate data
3. **Business Logic** → Service layer processes request
4. **Data Access** → Repository layer interacts with database
5. **Response** → Route layer returns HTTP response

## Design Principles

- **Single Responsibility**: Each layer has one clear purpose
- **Dependency Injection**: Clean dependency management
- **Type Safety**: Full type hints throughout
- **Error Handling**: Consistent error responses
- **Separation of Concerns**: Clear layer boundaries

## Geolocation Features

- **Automatic Geocoding**: Addresses automatically converted to coordinates
- **Haversine Distance**: Accurate distance calculations
- **Radius Queries**: Efficient spatial searches
- **Fallback Handling**: Graceful error handling for geocoding failures

## Performance Considerations

- **Database Indexing**: Optimized queries on coordinates
- **Bounding Box Filter**: Initial spatial filtering
- **Distance Calculation**: Only for filtered results
- **Connection Pooling**: Efficient database connections
