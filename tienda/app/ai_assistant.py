
from openai import OpenAI
from flask import current_app


def consultar_groq(mensajes):
    api_key = current_app.config.get("AI_API_KEY")
    api_url = current_app.config.get("AI_URL")
    modelo = current_app.config.get("AI_MODEL")

    if not api_key:
        raise RuntimeError(
            "No se encontró AI_API_KEY en el archivo .env"
        )

    cliente = OpenAI(
        api_key=api_key,
        base_url=api_url
    )

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        temperature=0.4,
        max_completion_tokens=1200
    )

    return respuesta.choices[0].message.content
