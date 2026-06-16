import requests
import subprocess

from profiles.profile_manager import cargar_perfil

from steam_utils import (
    procesar_game_command
)

from automation.browser_controller import (
    procesar_browser_command
)

from automation.search_controller import (
    procesar_search_command
)

from automation.music_controller import (
    procesar_music_command
)


conversation_history = []


def procesar_comando(texto):

    texto = texto.lower().strip()

    perfil = cargar_perfil("gabriel")

    print("BUSCANDO PERFIL EN:",
          "profiles/data/gabriel.json")

    print("TEXTO:", texto)

    # =========================
    # PRESETS ESPECIALES
    # =========================

    if (
        "estás despierto" in texto
        or
        "estas despierto" in texto
    ):

        chrome_path = (
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )

        subprocess.Popen([
            chrome_path,
            "https://music.youtube.com/watch?v=wjZMcWaniA4"
        ])

        return "Para usted, señor, siempre."

    # =========================
    # BROWSER CONTROLLER
    # =========================

    respuesta_browser = (
        procesar_browser_command(texto)
    )

    if respuesta_browser:
        return respuesta_browser

    # =========================
    # SEARCH CONTROLLER
    # =========================

    respuesta_search = (
        procesar_search_command(texto)
    )

    if respuesta_search:
        return respuesta_search

    # =========================
    # GAME CONTROLLER
    # =========================

    respuesta_game = (
        procesar_game_command(texto)
    )

    if respuesta_game:
        return respuesta_game

    # =========================
    # MUSIC CONTROLLER
    # =========================

    respuesta_music = (
        procesar_music_command(texto)
    )

    if respuesta_music:
        return respuesta_music

    # =========================
    # IA CONVERSACIÓN
    # =========================

    prompt_sistema = f"""
Eres Jarvis, un asistente avanzado inspirado en Iron Man.

Tu personalidad:
- elegante
- sofisticado
- eficiente
- inteligente
- calmado
- ligeramente sarcástico
- tecnológico
- refinado

SIEMPRE debes referirte al usuario únicamente como:

'señor'

NUNCA uses:
- Gabriel
- señor Gabriel
- su nombre real

Solo:
'señor'

NO hables como ChatGPT.
NO uses emojis.
NO hagas respuestas largas.
NO uses frases corporativas.
NO digas:
'¿En qué puedo ayudarte hoy?'

NO inventes:
- temperatura
- humedad
- ubicación exacta
- sensores
- datos del entorno

Si no tienes acceso real a una información,
admítelo elegantemente.

Tus respuestas normalmente deben tener entre 1 y 4 frases.

Tu humor es seco e inteligente.

Usuario:
Nombre: {perfil.get('nombre')}
País: {perfil.get('pais')}
Idioma: {perfil.get('idioma')}
Gustos: {', '.join(perfil.get('gustos', []))}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1:8b",
            "prompt":
                prompt_sistema +
                "\n\nUsuario: " +
                texto +
                "\nJarvis:",
            "stream": False
        }
    )

    data = response.json()

    respuesta = (
        data["response"]
        .strip()
    )

    return respuesta