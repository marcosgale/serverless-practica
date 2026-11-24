# Práctica integrada · del commit al despliegue

**Función:** `hello-fn` · AWS Lambda (Python, runtime administrado) · región `eu-north-1`
**Trigger:** Function URL pública (autenticación `NONE`)
**Pipeline:** GitHub Actions · `checkout → test → package → deploy`

## Entregables

| # | Entregable | Captura |
|---|------------|---------|
| 1 | Función ejecutándose | `capturas/1_funcion_ejecutandose.png` (+ logs: `capturas/1b_logs_cloudwatch.png`) |
| 2 | Pipeline en verde | `capturas/2_pipeline_verde.png` |
| 3 | Fallo bloqueado | `capturas/3_fallo_bloqueado.png` |
| 4 | Explicación commit → deploy | ver abajo |
| ★ | Reto extra (variable de entorno / secreto) | `capturas/4_reto_variable_entorno.png` |

## A · Qué gestiona el proveedor y qué gestiona el equipo

**AWS (proveedor) gestiona:** servidores físicos y virtuales, sistema operativo y parches, el runtime de Python (lo mantiene y corrige AWS al elegir "tiempo de ejecución administrado"), el escalado automático según peticiones, la alta disponibilidad, el endpoint HTTPS de la Function URL y la infraestructura de logs (CloudWatch).

**El equipo gestiona:** el código de la función y sus tests, las dependencias, la configuración (memoria, timeout, variables de entorno como `GREETING`), los permisos IAM (rol de ejecución de la función y el usuario `github-deployer` con el que despliega GitHub), la seguridad del acceso (decidimos que la URL sea pública con `NONE`), la gestión de secretos (claves de AWS en GitHub Secrets) y la pipeline de CI/CD.

## B · Ciclo commit → deploy (5 líneas)

1. Un miembro del equipo hace commit y push a `main`; GitHub Actions detecta el push y lanza la pipeline.
2. **Checkout + test:** se descarga el código en una máquina limpia y se ejecutan los tests con `pytest`; si alguno falla, la pipeline se detiene.
3. **Package:** solo si los tests pasan, se empaqueta `src/` en `function.zip`.
4. **Deploy:** con las credenciales guardadas en GitHub Secrets, se sube el zip a la Lambda `hello-fn` con `aws lambda update-function-code`.
5. **Smoke test:** se invoca la función desplegada y se comprueba que responde `200`; la nueva versión ya está disponible en la Function URL.

## Cómo se provocó el fallo bloqueado

En `src/lambda_function.py` se cambió `"statusCode": 200` por `"statusCode": 500` y se hizo push. Los tests fallaron, `package` y `deploy` quedaron en *skipped* y la Function URL siguió sirviendo la versión anterior. Después se revirtió el cambio.

## Reto extra

- El saludo se lee de la variable de entorno `GREETING` (Lambda → Configuración → Variables de entorno), no está escrito en el código: con `GREETING=Buenas` la URL devuelve `Buenas, Ana!` sin tocar el código.
- Las claves de AWS (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) están en GitHub Secrets; nunca aparecen en el repositorio.
