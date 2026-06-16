print("Jarvis iniciado correctamente")

from PySide6.QtCore import QThread, Signal
from web_utils import buscar_web
import speech_recognition as sr
import traceback
import threading

from jarvis_core import procesar_comando

from tts_engine import (
    hablar_edge as hablar,
    detener_habla
)


class JarvisWorker(QThread):
    state_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True


    def run(self):
        try:
            print("WORKER INICIADO")

            print("Inicializando reconocimiento de voz...")

            r = sr.Recognizer()

            r.pause_threshold = 1.8

            print("Intentando acceder al micrófono...")

            with sr.Microphone() as source:
                print("MICRÓFONO DETECTADO")

                r.adjust_for_ambient_noise(source, duration=0.1)

                while self.running:
                    try:
                        print("ESCUCHANDO...")
                        self.state_changed.emit("listening")

                        try:
                            audio = r.listen(
                                source,
                                timeout=8,
                                phrase_time_limit=20
                            )
                            
                            texto = r.recognize_google(audio, language="es-ES")
                            print("RECONOCIÓ:", texto)

                            texto_lower = texto.lower().strip()


                        except sr.WaitTimeoutError:
                            print("No se detectó voz...")
                            continue
                            

                        print("AUDIO CAPTURADO")


                        palabras_stop = ["para", "silencio", "cállate", "callate", "detente"]

                        if any(palabra in texto_lower for palabra in palabras_stop):
                            print("INTERRUPCIÓN DETECTADA")
                            detener_habla()
                            self.state_changed.emit("idle")
                            continue

                        if "jarvis" not in texto_lower:
                            self.state_changed.emit("idle")
                            continue

                        self.state_changed.emit("thinking")

                        comando = texto_lower.replace("jarvis", "").strip()

                        respuesta = procesar_comando(comando)

                        print("RESPUESTA:", respuesta)

                        self.state_changed.emit("speaking")

                        hablar(respuesta)
                        
                        self.state_changed.emit("idle")

                    except sr.UnknownValueError:
                        self.state_changed.emit("idle")
                        continue

                    except Exception:
                        print("ERROR INTERNO:")
                        traceback.print_exc()
                        self.state_changed.emit("idle")

        except Exception:
            print("\n💥 ERROR GRAVE EN WORKER:\n")
            traceback.print_exc()
            input("Presiona ENTER...")


    def stop(self):
        self.running = False