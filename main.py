from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
from prometheus_client.asgi import make_asgi_app
from starlette.middleware.base import BaseHTTPMiddleware
import time
from pydantic import BaseModel

class Element(BaseModel):
    element: str
class Expression(BaseModel):
    expr: str

app = FastAPI()

# Создаём метрики
http_requests_total = Counter(
    'http_requests_total', 'Number of HTTP requests received', ['method', 'endpoint']
)
http_requests_milliseconds = Histogram(
    'http_requests_milliseconds', 'Duration of HTTP requests in milliseconds', ['method', 'endpoint']
)
last_sum1n = Gauge('last_sum1n', 'Value stores last result of sum1n')
last_fibo = Gauge('last_fibo', 'Value stores last result of fibo')
list_size = Gauge('list_size', 'Value stores current list size')
last_calculator = Gauge('last_calculator', 'Value stores last result of calculator')
errors_calculator_total = Counter('errors_calculator_total', 'Number of errors in calculator')

# Middleware для сбора метрик
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path

        start_time = time.time()
        try:
            response = await call_next(request)
        finally:
            duration = (time.time() - start_time) * 1000  # Перевод в миллисекунды
            http_requests_total.labels(method=method, endpoint=endpoint).inc()
            http_requests_milliseconds.labels(method=method, endpoint=endpoint).observe(duration)
        return response

app.add_middleware(MetricsMiddleware)

# Обновляем метрики в роуте /sum1n/{n}
@app.get("/sum1n/{n}")
def sum1n(n: int):
    total = sum(range(1, n + 1))
    last_sum1n.set(total)
    return {"result": total}

# Обновляем метрики в роуте /fibo
@app.get("/fibo")
def fibo(n: int):
    if n <= 0:
        result = 0
    elif n == 1:
        result = 0
    elif n == 2:
        result = 1
    else:
        a, b = 0, 1
        for _ in range(2, n):
            a, b = b, a + b
        result = b

    last_fibo.set(result)
    return {"result": result}

# Обновляем метрики в роуте /list
global_list = []

@app.put("/list")
def add_to_list(item: Element):
    global global_list
    global_list.append(item.element)
    list_size.set(len(global_list))
    return {"result": global_list}

# Обновляем метрики в роуте /calculator
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
                errors_calculator_total.inc()
                return JSONResponse(status_code=403, content={"error": "zerodiv"})
            result = num1 / num2
        else:
            errors_calculator_total.inc()
            return JSONResponse(status_code=400, content={"error": "invalid"})
        
        last_calculator.set(result)
        return {"result": result}
    except ValueError:
        errors_calculator_total.inc()
        return JSONResponse(status_code=400, content={"error": "invalid"})

# Добавляем экспортёр Prometheus по роуту /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
