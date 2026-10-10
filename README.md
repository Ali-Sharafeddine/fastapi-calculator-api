# FastAPI Calculator API

A small REST API built with FastAPI as part of my Python and AI Engineering learning journey.

The project demonstrates:

- REST API fundamentals
- FastAPI endpoints
- Query parameters
- Python type hints
- JSON responses
- HTTP status codes
- Error handling with `HTTPException`
- API testing with `pytest`
- FastAPI `TestClient`

## Endpoints

### Health Check

```http
GET /health


## POST Request with Pydantic Validation

The API also supports structured JSON requests through:

POST /calculate

Example request:

```json
{
  "a": 10,
  "b": 5,
  "operation": "add"
}