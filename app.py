import json
from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Cargar conocimientos
with open("conocimientos.json", "r") as f:
    conocimientos = json.load(f)

# Crear pipeline de Hugging Face para generación de texto
generator = pipeline("text-generation", model="distilgpt2")

@app.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "POST":
        edad = int(request.form["edad"])
        objetivo = request.form["objetivo"]
        tiempo = int(request.form["tiempo"])
        objetivo_lower = objetivo.lower()

        # Clasificación con razonamiento
        if any(palabra in objetivo_lower for palabra in conocimientos["objetivos_imposibles"]):
            categoria = "Imposible"
            explicacion = generator(
                f"Explica por qué '{objetivo}' es imposible:",
                max_length=60,
                do_sample=True
            )[0]["generated_text"]

            return render_template(
                "resultado.html",
                objetivo=objetivo,
                categoria=categoria,
                explicacion=explicacion,
                intensidad=None,
                recomendacion_extra=None,
                puntuacion=0
            )

        elif any(palabra in objetivo_lower for palabra in conocimientos["objetivos_realistas"]):
            categoria = "Realista"
            explicacion = generator(
                f"Explica cómo lograr '{objetivo}' de manera realista:",
                max_length=100,
                do_sample=True
            )[0]["generated_text"]

        else:
            categoria = "Desconocido"
            explicacion = generator(
                f"No tengo suficiente información sobre '{objetivo}', explica de forma segura:",
                max_length=60,
                do_sample=True
            )[0]["generated_text"]

        # Generar plan según tiempo
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
    app.run(host="0.0.0.0", debug=True)
    