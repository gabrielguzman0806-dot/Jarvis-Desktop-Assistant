import subprocess
import urllib.parse


chrome_path = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)


music_keywords = [
    "pon",
    "reproduce",
    "toca",
    "quiero escuchar",
    "ponme",
    "escucha"
]


def procesar_music_command(texto):

    texto = texto.lower()

    if not any(
        k in texto
        for k in music_keywords
    ):
        return None

    texto_limpio = texto

    for keyword in music_keywords:
        texto_limpio = texto_limpio.replace(
            keyword,
            ""
        )

    texto_limpio = texto_limpio.replace(
        "okay",
        ""
    )

    texto_limpio = texto_limpio.replace(
        "ok",
        ""
    )

    texto_limpio = texto_limpio.strip()

    if not texto_limpio:
        texto_limpio = "musica"

    query = urllib.parse.quote(
        texto_limpio
    )

    youtube_url = (
        "https://www.youtube.com/results"
        f"?search_query={query}"
    )

    subprocess.Popen([
        chrome_path,
        youtube_url
    ])

    return (
        f"Reproduciendo {texto_limpio}, señor."
    )