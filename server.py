from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el cliente web


@app.route("/api/calcular-ganancia", methods=["POST"])
def calcular_ganancia():
  data = request.get_json()

  if not data or "capital" not in data:
    return jsonify({"error": "El campo 'capital' es requerido."}), 400

  try:
    capital = float(data["capital"])
    if capital <= 0:
      return (
          jsonify({"error": "El capital debe ser un número mayor a cero."}),
          400,
      )

    tasa_mensual = 0.02  # 2% mensual
    ganancia = capital * tasa_mensual
    total_acumulado = capital + ganancia

    return (
        jsonify({
            "capital_inicial": capital,
            "tasa_interes": "2%",
            "ganancia_mes": ganancia,
            "total_acumulado": total_acumulado,
        }),
        200,
    )

  except ValueError:
    return (
        jsonify({
            "error": "El valor ingresado para el capital no es válido."
        }),
        400,
    )


if __name__ == "__main__":
  # El servidor escucha peticiones en el puerto 5000
  app.run(host="0.0.0.0", port=5000, debug=True)