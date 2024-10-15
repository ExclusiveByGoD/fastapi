from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

global_list = []

@app.get("/sum1n/{n}")
def sum1n(n: int):
    total = sum(range(1, n+1))
    return {"result": total}

@app.get("/fibo")
def fibo(n: int):
    if n <= 0:
        return {"result": 0}
    elif n == 1:
        return {"result": 0}
    elif n == 2:
        return {"result": 1}
    else:
        a, b = 0, 1
        for _ in range(2, n):
            a, b = b, a + b
        return {"result": b}

@app.post("/reverse")
def reverse(string: Optional[str] = Header(None)):
    if string is None:
        raise HTTPException(status_code=400, detail="Header 'string' not provided")
    reversed_string = string[::-1]
    return {"result": reversed_string}

class Element(BaseModel):
    element: str

@app.put("/list")
def add_to_list(item: Element):
    global global_list
    global_list.append(item.element)
    return {"result": global_list}

@app.get("/list")
def get_list():
    return {"result": global_list}

class Expression(BaseModel):
    expr: str

@app.post("/calculator")
def calculator(expression: Expression):
    expr = expression.expr
    try:
        num1_str, operator, num2_str = expr.split(',')
        num1 = float(num1_str)
        num2 = float(num2_str)
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return JSONResponse(status_code=403, content={"error": "zerodiv"})
            result = num1 / num2
        else:
            return JSONResponse(status_code=400, content={"error": "invalid"})
        return {"result": result}
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "invalid"})
