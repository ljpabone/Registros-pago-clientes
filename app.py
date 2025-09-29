from flask import Flask, render_template, request, redirect
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
DATA_FOLDER = "clientes"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/crear_cliente", methods=["POST"])
def crear_cliente():
    nombre = request.form["nombre"]
    cedula = request.form["cedula"]
    telefono = request.form["telefono"]
    ciudad = request.form["ciudad"]
    monto = float(request.form["monto"])
    dias = int(request.form["dias"])
    seguro = request.form.get("seguro", "No")
    plazo = request.form["plazo"]
    cuota_diaria = float(request.form["cuota_diaria"])

    filename = f"{DATA_FOLDER}/{cedula}_{nombre}.xlsx"
    if not os.path.exists(filename):
        df_info = pd.DataFrame([{
            "Nombre": nombre,
            "Cédula": cedula,
            "Teléfono": telefono,
            "Ciudad": ciudad,
            "Monto del préstamo": monto,
            "Días de pago": dias,
            "Seguro": seguro,
            "Plazo": plazo,
            "Cuota diaria": cuota_diaria
        }])
        df_pagos = pd.DataFrame(columns=["Fecha", "Valor pagado"])
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            df_info.to_excel(writer, sheet_name="Datos del cliente", index=False)
            df_pagos.to_excel(writer, sheet_name="Pagos", index=False)
    return redirect("/")

@app.route("/registrar_pago", methods=["POST"])
def registrar_pago():
    cedula = request.form["cedula_buscar"]
    nombre = request.form["nombre_buscar"]
    fecha = request.form["fecha"]
    valor = float(request.form["valor"])

    filename = f"{DATA_FOLDER}/{cedula}_{nombre}.xlsx"
    if os.path.exists(filename):
        df_pagos = pd.read_excel(filename, sheet_name="Pagos", engine="openpyxl")
        df_pagos = pd.concat([df_pagos, pd.DataFrame([{"Fecha": fecha, "Valor pagado": valor}])], ignore_index=True)
        with pd.ExcelWriter(filename, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df_pagos.to_excel(writer, sheet_name="Pagos", index=False)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
