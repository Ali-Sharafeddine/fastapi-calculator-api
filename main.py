from fastapi import FastAPI, HTTPException
app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/add")
def add(a: float, b: float):
    result = a + b

    return {
        "operation": "addition",
        "result": result
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