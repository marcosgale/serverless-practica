import json
import os


def _get_name(event):
    """Busca el nombre en query string, body o directamente en el evento."""

    # 1. Query string
    query = event.get("queryStringParameters") or {}
    name = query.get("name") or query.get("nombre")

    if name:
        return name

    # 2. Body JSON
    body = event.get("body")

    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            body = {}

    if isinstance(body, dict):
        name = body.get("name") or body.get("nombre")

        if name:
            return name

    # 3. Invocación directa
    return event.get("name") or event.get("nombre") or "mundo"


def lambda_handler(event, context):
    """Función hello."""

    event = event or {}
    name = _get_name(event)

    greeting = os.environ.get("GREETING", "Hola")

    print(f"Evento recibido: {json.dumps(event, default=str)}")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": f"{greeting}, {name}!"
        }),
    }