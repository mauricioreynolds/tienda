
from app import create_app
from app.ai_assistant import consultar_groq

app = create_app()

with app.app_context():
    try:
        respuesta = consultar_groq([
            {
                "role": "system",
                "content": "Eres el asistente inteligente de Mi Tienda."
            },
            {
                "role": "user",
                "content": "Preséntate y explica brevemente cómo puedes ayudar a un micromercado."
            }
        ])

        print("\nCONEXIÓN CON GROQ EXITOSA")
        print("--------------------------------")
        print(respuesta)

    except Exception as error:
        print("\nERROR AL CONECTAR CON GROQ")
        print(error)
