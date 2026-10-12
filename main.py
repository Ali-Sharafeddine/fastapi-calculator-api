from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

from database import (
    create_table,
    save_calculation,
    get_calculations,
    get_calculations_count
)

from typing import Literal
from pydantic import BaseModel

create_table()

class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: Literal["add", "subtract", "divide"]
    

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/add")
def add(a: float, b: float):
    return {
        "operation": "addition",
        "result": a + b
    }


@app.get("/subtract")
def subtract(a: float, b: float):
    return {
        "operation": "subtraction",
        "result": a - b
    }


@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot divide by zero."
        )

    return {
        "operation": "division",
        "result": a / b
    }


@app.get("/calculations")
def calculations():
    rows = get_calculations()

    return {
        "calculations": rows
    }


@app.post("/calculate")
def calculate(request: CalculationRequest):

    if request.operation == "add":
        result = request.a + request.b

    elif request.operation == "subtract":
        result = request.a - request.b

    elif request.operation == "divide":
        if request.b == 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot divide by zero."
            )

        result = request.a / request.b

    save_calculation(
        request.a,
        request.b,
        request.operation,
        result
    )

    return {"result": result}


@app.get("/calculations/count")
def calculations_count():
    count = get_calculations_count()

    return {
        "count": count
    }