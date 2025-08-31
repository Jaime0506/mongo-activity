# 🚗 Car Management API

A modern RESTful API built with FastAPI and MongoDB for managing car inventory. This project demonstrates best practices in API development with async/await patterns, Pydantic validation, and MongoDB integration.

## 🎯 Features

-   **CRUD Operations**: Complete Create, Read, Update, Delete operations for cars
-   **Data Validation**: Robust validation using Pydantic models with custom field constraints
-   **MongoDB Integration**: Async MongoDB operations using Motor driver
-   **Plate Validation**: Colombian license plate format validation (ABC123)
-   **Duplicate Prevention**: Prevents duplicate license plates
-   **Async Architecture**: Full async/await implementation for optimal performance
-   **Environment Configuration**: Flexible configuration using environment variables

## 🏗️ Architecture

```
mongo_activity/
├── main.py              # FastAPI application entry point
├── config/
│   ├── config.py        # Application settings and configuration
│   ├── database.py      # MongoDB connection management
│   └── __init__.py
├── models/
│   ├── Car.py          # Pydantic models for car data
│   └── _init__.py
├── routes/
│   └── router_car.py   # Car management API endpoints
└── venv/               # Virtual environment
```

## 🚀 Quick Start

### Prerequisites

-   Python 3.8+
-   MongoDB instance (local or cloud)
-   Virtual environment

### Installation

1. **Clone and navigate to the project:**

    ```bash
    cd mongo_activity
    ```

2. **Create and activate virtual environment:**

    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install fastapi uvicorn motor pymongo pydantic pydantic-settings
    ```

4. **Create environment file:**

    ```bash
    # Create .env file with your MongoDB configuration
    echo "MONGODB_URI=mongodb://localhost:27017" > .env
    echo "MONGODB_DB=cardb" >> .env
    echo "MONGODB_COLLECTION_CARS=cars" >> .env
    ```

5. **Run the application:**

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

6. **Access the API:**
    - API Documentation: http://localhost:8000/docs
    - Alternative Docs: http://localhost:8000/redoc
    - Health Check: http://localhost:8000/

## 📋 API Endpoints

### Cars Management

| Method   | Endpoint         | Description                     |
| -------- | ---------------- | ------------------------------- |
| `POST`   | `/cars/`         | Create a new car                |
| `GET`    | `/cars/`         | List all cars (with pagination) |
| `GET`    | `/cars/{car_id}` | Get car by ID                   |
| `PATCH`  | `/cars/{car_id}` | Update car (partial)            |
| `DELETE` | `/cars/{car_id}` | Delete car                      |

### Request/Response Examples

#### Create Car

```bash
POST /cars/
Content-Type: application/json

{
  "year": 2023,
  "model_name": "Toyota Corolla",
  "description": "Sedán compacto con excelente economía de combustible",
  "plate": "ABC123"
}
```

#### Response

```json
{
    "_id": "507f1f77bcf86cd799439011",
    "year": 2023,
    "model_name": "Toyota Corolla",
    "description": "Sedán compacto con excelente economía de combustible",
    "plate": "ABC123"
}
```

#### List Cars

```bash
GET /cars/?limit=10
```

#### Update Car

```bash
PATCH /cars/507f1f77bcf86cd799439011
Content-Type: application/json

{
  "year": 2024,
  "description": "Sedán compacto actualizado con nuevas características"
}
```

## 🔧 Data Models

### Car Model

```python
class Car(BaseModel):
    year: int = Field(..., gt=2000, description="Año del modelo, debe ser mayor a 2000")
    model_name: str = Field(..., min_length=5, description="Nombre del modelo (mínimo 5 caracteres)")
    description: str = Field(..., min_length=10, description="Descripción del carro (mínimo 10 caracteres)")
    plate: str = Field(..., min_length=6, max_length=6, pattern="^[A-Z]{3}[0-9]{3}$", description="Placa colombiana en formato ABC123")
```

### Validation Rules

-   **Year**: Must be greater than 2000
-   **Model Name**: Minimum 5 characters
-   **Description**: Minimum 10 characters
-   **Plate**: Colombian format (3 letters + 3 numbers, e.g., ABC123)

## ⚙️ Configuration

The application uses `pydantic-settings` for configuration management. Key settings:

### Environment Variables

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=cardb
MONGODB_COLLECTION_CARS=cars

# Alternative: Individual components
MONGODB_HOST=prueba.gqpx3rt.mongodb.net
MONGODB_USER=your_username
MONGODB_PASSWORD=your_password
MONGODB_PARAMS=retryWrites=true&w=majority

# App Configuration
APP_NAME=CarAPI
APP_ENV=dev
APP_HOST=127.0.0.1
APP_PORT=8000
```

## 🗄️ Database Schema

### Cars Collection

```json
{
    "_id": "ObjectId",
    "year": "int (>= 2000)",
    "model_name": "string (>= 5 chars)",
    "description": "string (>= 10 chars)",
    "plate": "string (ABC123 format)"
}
```

## 🔒 Error Handling

The API provides comprehensive error handling:

-   **400 Bad Request**: Invalid input data or malformed requests
-   **404 Not Found**: Car not found by ID
-   **409 Conflict**: Duplicate license plate
-   **422 Unprocessable Entity**: Validation errors

### Error Response Format

```json
{
    "detail": "Error message description"
}
```

## 🧪 Testing

### Manual Testing with curl

```bash
# Create a car
curl -X POST "http://localhost:8000/cars/" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2023,
    "model_name": "Honda Civic",
    "description": "Sedán confiable con buen rendimiento",
    "plate": "XYZ789"
  }'

# List cars
curl -X GET "http://localhost:8000/cars/"

# Get specific car
curl -X GET "http://localhost:8000/cars/{car_id}"

# Update car
curl -X PATCH "http://localhost:8000/cars/{car_id}" \
  -H "Content-Type: application/json" \
  -d '{"year": 2024}'

# Delete car
curl -X DELETE "http://localhost:8000/cars/{car_id}"
```

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Set production MongoDB URI and credentials
2. **CORS**: Configure CORS for your frontend domain
3. **Rate Limiting**: Implement rate limiting for API protection
4. **Logging**: Add structured logging for monitoring
5. **Health Checks**: Implement health check endpoints

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📚 Dependencies

-   **FastAPI**: Modern web framework for building APIs
-   **Uvicorn**: ASGI server for running FastAPI applications
-   **Motor**: Async MongoDB driver
-   **Pymongo**: MongoDB driver (used by Motor)
-   **Pydantic**: Data validation and settings management
-   **Pydantic-settings**: Settings management with environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For questions or issues:

1. Check the API documentation at `/docs`
2. Review the error messages in the response
3. Check the application logs for debugging information

---

**Built with ❤️ using FastAPI and MongoDB**
