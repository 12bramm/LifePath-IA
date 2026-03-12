import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Cargar conocimientos
with open("conocimientos.json", "r") as f:
    conocimientos = json.load(f)


@app.route("/", methods=["GET", "POST"])
def inicio():

    if request.method == "POST":

        edad = int(request.form["edad"])
        objetivo = request.form["objetivo"]
        tiempo = int(request.form["tiempo"])

        objetivo_lower = objetivo.lower()

        # CLASIFICACIÓN DEL OBJETIVO
        if any(palabra in objetivo_lower for palabra in conocimientos["objetivos_imposibles"]):
            categoria = "Imposible"
            explicacion = "Este objetivo está clasificado como imposible según el conocimiento del sistema."

        elif any(palabra in objetivo_lower for palabra in conocimientos["objetivos_realistas"]):
            categoria = "Realista"
            explicacion = "Este objetivo es alcanzable con planificación y esfuerzo."

        elif "millonario en un día" in objetivo_lower:
            categoria = "Extremadamente improbable"
            explicacion = "Aunque no es físicamente imposible, es extremadamente improbable."

        else:
            categoria = "Desconocido"
            explicacion = "El sistema no tiene suficiente información sobre este objetivo."

        # SI ES IMPOSIBLE
        if categoria == "Imposible":
            return render_template(
                "resultado.html",
                objetivo=objetivo,
                categoria=categoria,
                explicacion=explicacion,
                intensidad=None,
                recomendacion_extra=None,
                puntuacion=0
            )

        # PLAN PARA OBJETIVOS POSIBLES
        if tiempo < 5:
            intensidad = "Progreso lento pero constante"
        elif tiempo < 10:
            intensidad = "Progreso moderado"
        else:
            intensidad = "Progreso rápido e intensivo"

        if edad < 18:
            recomendacion_extra = "Aprovecha tu etapa de aprendizaje rápido."
        else:
            recomendacion_extra = "Organiza bien tu tiempo con responsabilidades."

        puntuacion = min(100, tiempo * 10)

        return render_template(
            "resultado.html",
            objetivo=objetivo,
            intensidad=intensidad,
            recomendacion_extra=recomendacion_extra,
            puntuacion=puntuacion,
            categoria=categoria,
            explicacion=explicacion
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)