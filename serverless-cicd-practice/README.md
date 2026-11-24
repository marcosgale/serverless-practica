# serverless-cicd-practice

Función serverless "hello" en AWS Lambda (Python) desplegada con GitHub Actions.

## Pipeline

checkout → test → package → deploy

### test
Instala dependencias y ejecuta pytest.

### package
Comprime src/ en function.zip, únicamente si los tests pasan.

### deploy
Despliega el ZIP en AWS Lambda y realiza una prueba de ejecución.

El despliegue se realiza únicamente cuando hay un push a main y los tests han pasado.

## Configuración en GitHub

En:

Settings → Secrets and variables → Actions

### Secrets

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

### Variables opcionales

- LAMBDA_FUNCTION_NAME
- AWS_REGION

Por defecto:

- Lambda: hello-fn
- Región: eu-north-1

## Probar localmente

```bash
pip install -r requirements.txt
pytest -v tests/