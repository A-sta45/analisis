# Análisis

Conjunto de ejercicios y pequeños proyectos de análisis de algoritmos y arquitectura cliente-servidor en Python.

## Contenido

- **`analizar_tiempois.py`** — función que recorre un arreglo de tiempos de respuesta y devuelve el valor máximo, su primera posición y cuántas veces aparece, en un solo recorrido O(n).
- **`banco.py`** — módulo de transferencias bancarias con **control optimista de concurrencia (OCC)**: validación de reglas de negocio, manejo de idempotencia (evita procesar dos veces la misma solicitud) y reintentos ante conflictos de versión.
- **`servidor.py`** / **`cliente.py`** — arquitectura cliente-servidor con **sockets TCP**: el cliente envía un capital a invertir, el servidor calcula una ganancia del 2% mensual y devuelve el resumen.
- **`server.py`** — la misma lógica de cálculo de ganancia expuesta como API REST con **Flask**, pensada para ser consumida desde `index.html`.
- **`index.html`** — interfaz web simple que consume la API de `server.py`.

## Ejecución

Cliente/servidor por sockets:

```bash
python servidor.py   # terminal 1
python cliente.py    # terminal 2
```

API Flask + interfaz web:

```bash
pip install flask flask-cors
python server.py
# abrir index.html en el navegador
```
