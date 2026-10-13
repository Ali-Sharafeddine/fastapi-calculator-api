from fastapi import FastAPI, HTTPException
from schemas import CalculationRequest
from services import calculate_result
from database import (
    create_table,
    save_calculation,
    get_calculations,
    get_calculations_count,
    delete_calculation
)


app = FastAPI()
create_table()
    

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/add")
def add(a: float, b: float):
    return {
        "operation": "addition",
        "result": calculate_result(a, b, "add")
    }


@app.get("/subtract")
def subtract(a: float, b: float):
    return {
        "operation": "subtraction",
        "result": calculate_result(a, b, "subtract")
    }


@app.get("/divide")
def divide(a: float, b: float):
    try:
        result = calculate_result(a, b, "divide")

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "operation": "division",
        "result": result
    }


@app.get("/calculations")
def calculations():
    rows = get_calculations()

    return {
        "calculations": rows
    }


@app.post("/calculate")
def calculate(request: CalculationRequest):
    try:
        result = calculate_result(
            request.a,
            request.b,
            request.operation
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

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


@app.delete("/calculations/{calculation_id}")
def remove_calculation(calculation_id: int):
    deleted = delete_calculation(calculation_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found."
        )

    return {"deleted_id": calculation_id}