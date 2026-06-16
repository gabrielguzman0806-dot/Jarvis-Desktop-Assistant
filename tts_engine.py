import pygame
import asyncio
import edge_tts
import time

pygame.mixer.init()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def generar_voz(texto):

    communicate = edge_tts.Communicate(
        text=texto,
        voice="en-US-AndrewMultilingualNeural",
        pitch="-15Hz",
        rate="+20%"
    )

    output_path = f"temp_voice_{int(time.time() * 1000)}.mp3"

    await communicate.save(output_path)

    return output_path


def hablar_edge(texto):

    texto = texto.replace("**", "")
    texto = texto.replace("*", "")
    texto = texto.replace("#", "")
    texto = texto.replace("```", "")

    texto = texto.replace("Jarvis", "Yarvis")

    texto = texto.encode(
        "cp1252",
        errors="ignore"
    ).decode("cp1252")

    output_path = loop.run_until_complete(
        generar_voz(texto)
    )

    pygame.mixer.music.stop()

    pygame.mixer.music.load(output_path)

    pygame.mixer.music.play()


def detener_habla():

    try:

        pygame.mixer.music.stop()

    except:
        pass