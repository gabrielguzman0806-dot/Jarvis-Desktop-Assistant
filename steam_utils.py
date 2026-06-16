import subprocess

from ai.game_intent_ai import (
    interpretar_juego
)


games = {

    "marvel rivals":
        "steam://rungameid/2767030",

    "helldivers 2":
        "steam://rungameid/553850",

    "gta 5":
        "steam://rungameid/271590",

    "cyberpunk":
        "steam://rungameid/1091500"
}


jugar_keywords = [
    "juega",
    "jugar",
    "inicia",
    "lanza",
    "quiero jugar",
    "despliega"
]


def procesar_game_command(texto):

    texto = texto.lower()

    print("ENTRANDO A GAME CONTROLLER")
    print("TEXTO RECIBIDO:", texto)

    if not any(
        k in texto
        for k in jugar_keywords
    ):
        return None

    juego_interpretado = (
        interpretar_juego(texto)
    )

    print(
        "JUEGO INTERPRETADO:",
        juego_interpretado
    )

    for game, url in games.items():

        if game in juego_interpretado:

            subprocess.Popen(
                [
                    "cmd",
                    "/c",
                    "start",
                    url
                ],
                shell=True
            )

            return (
                f"Preparando {game}, señor."
            )

    return (
        "No encontré ese juego, señor."
    )