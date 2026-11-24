import json
import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from lambda_function import lambda_handler


def test_saludo_por_defecto(monkeypatch):
    monkeypatch.delenv("GREETING", raising=False)

    resp = lambda_handler({}, None)

    assert resp["statusCode"] == 200

    assert json.loads(resp["body"])["message"] == "Hola, mundo!"


def test_saludo_con_nombre():
    resp = lambda_handler({"name": "UCJC"}, None)

    assert "UCJC" in json.loads(resp["body"])["message"]


def test_saludo_desde_body_http():
    resp = lambda_handler(
        {"body": json.dumps({"name": "Ana"})},
        None
    )

    assert "Ana" in json.loads(resp["body"])["message"]


def test_saludo_desde_query_string_url():
    resp = lambda_handler(
        {"queryStringParameters": {"nombre": "Ana"}},
        None
    )

    assert resp["statusCode"] == 200

    assert "Ana" in json.loads(resp["body"])["message"]


def test_greeting_desde_variable_de_entorno(monkeypatch):
    monkeypatch.setenv("GREETING", "Buenas")

    resp = lambda_handler({"name": "Ana"}, None)

    assert json.loads(resp["body"])["message"] == "Buenas, Ana!"