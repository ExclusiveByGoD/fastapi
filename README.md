# fastapi-final
## Инструкция к запуску
### Требования

- Python3.6+, т.е. версия языка Python от 3.6 и выше
- pip, менеджер пакетов Python

### Запуск

Перед тем, как начать разработку API нужно подготовить окружение для проекта. В этом
окружении будут храниться зависимые пакеты.

> 🕹 Запускайте следующие шаги на своем компьютере

#### 1. Установим окружение.

Окружение будет находиться в папке `.venv`. В нем будут храниться нужная версия питона
и все установленные пакеты.

```bash
python3 -m venv .venv
```

#### 2. Активируем окружение.

Теперь когда будете запускать данный проект, то всегда нужно активировать именно текущее окружение.

```bash
source .venv/bin/activate
```

Это удобно - держать отдельные окружения в папках проекта. Тогда не будут смешиваться
зависимости проекта. Это помогает нам избегать dependency hell, когда установлено очень много как
нужных, так и ненужных пакетов. Также, это помогает избегать конфликта версий пакетов.

#### 3. Установим зависимости

```bash
pip install -r requirements.txt
```

#### 4. Запустим API

```bash
uvicorn main:app --reload
```

## Примеры запросов

`/sum1n`, принимающий GET запросы.

Передается число n через URL. Вернуть сумму от 1 до n.

Пример запроса.

```bash
$ curl http://localhost:8000/sum1n/10
{"result": 55}
```

---

`/fibo`, принимающий GET запросы.

Передается число n через URL Query. Вернуть n-ное число из последовательности Фибоначчи.

Пример запроса.

```bash
$ curl http://localhost:8000/fibo?n=5
{"result": 3}
```

---

`/reverse`, принимающий POST запросы.

Передается строка `string` через Header. Вернуть перевернутую строку задом наперед.

Пример запроса.

```bash
$ curl -X POST -H "string: hello" http://localhost:8000/reverse
{"result": "olleh"}
```

---

`/list`, принимающий PUT запросы.

Передается строка `element` через JSON тело запроса. Сохранить строку `element` в глобальный массив.

Пример запроса.

```bash
$ curl -X PUT -d '{"element":"Apple"}' -H 'Content-Type: application/json' http://localhost:8000/list
$ curl -X PUT -d '{"element":"Microsoft"}' -H 'Content-Type: application/json' http://localhost:8000/list
$ curl http://localhost:8000/list
{"result": ["Apple", "Microsoft"]}
```

---

`/list`, принимающий GET запросы.

Вернуть глобальный массив.

Пример запроса.

```bash
$ curl http://localhost:8000/list
{"result": []}
$ curl -X PUT -d '{"element":"Apple"}' -H 'Content-Type: application/json' http://localhost:8000/list
$ curl -X PUT -d '{"element":"Microsoft"}' -H 'Content-Type: application/json' http://localhost:8000/list
$ curl http://localhost:8000/list
{"result": ["Apple", "Microsoft"]}
```

---

`/calculator`, принимающий POST запросы.

Передается строка `expr` через JSON тело запроса. Строка `expr` состоит из математического выражения, которое нужно вычислить. Формат строки следующий: `num1,operator,num2`.

- `num1` и `num2` - это числа
- `operator` - это математическая операция: +,-,/,\*

Вернуть результат математического выражения.

Если `expr` неверного формата, вернуть `{"error": "invalid"}` со статусом `400 Bad Request`.

При делении на ноль вернуть `{"error": "zerodiv"}` со статусом `403`.

Пример запроса.

```bash
$ curl -X POST -d '{"expr": "1,+,1"}' -H 'Content-Type: application/json' http://localhost:8000/calculator
{"result": 2}
```

