import io
import json
import logging
import os
import wave
from io import BytesIO
from typing import Any, Dict

import uvicorn
from fastapi import Body, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
from vosk import KaldiRecognizer, Model

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Audio Transcription Service",
    description="Сервис расшифровки аудиозаписей с использованием Vosk",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Путь к модели Vosk
# VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", (Path(
#     __file__).parent.parent / "models" / 'vosk-model-ru-0.42').as_posix())
VOSK_MODEL_DIR = os.getenv("VOSK_MODEL_DIR", '')
VOSK_MODEL_NAME = os.getenv("VOSK_MODEL_NAME", '')
assert VOSK_MODEL_NAME
assert VOSK_MODEL_DIR
VOSK_MODEL_PATH = VOSK_MODEL_DIR + '/' + VOSK_MODEL_NAME

# Глобальная переменная для хранения модели
MODEL = None


@app.on_event("startup")
async def load_model():
    """Загрузка модели Vosk при старте приложения"""
    global MODEL
    print(f"Загрузка модели Vosk из {VOSK_MODEL_PATH}")
    MODEL = Model(VOSK_MODEL_PATH)
    print("Модель Vosk успешно загружена")


@app.get("/")
async def root():
    return {"message": "Audio Transcription Service is running"}


@app.post("/decode/file")
async def decode_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Эндпоинт для расшифровки аудиофайла
    Ожидает файл в формате, поддерживаемом ffmpeg
    Возвращает JSON с результатом расшифровки
    """

    # Проверка загрузки модели
    if MODEL is None:
        return {
            "status": "Ошибка",
            "content": "Модель распознавания речи не загружена"
        }

    content = await file.read()
    await file.close()
    audio_data = io.BytesIO(content)
    try:
        audio = AudioSegment.from_file(audio_data)
        text = decode_recording(
            model=MODEL, data=audio.export(format="wav").read())
        return {
            'status': 'success',
            'data': text
        }
    except Exception as e:
        logger.error(f"Error in decode_file endpoint: {str(e)}", exc_info=True)
        return {
            'status': 'error',
            'data': str(e)
        }


@app.post("/decode/bytes")
async def decode_bytes(data: bytes = Body(...)) -> Dict[str, Any]:
    """
    Эндпоинт для расшифровки аудиоданных в формате байтов
    Ожидает байты аудио в формате, поддерживаемом pydub
    Возвращает JSON с результатом расшифровки
    """

    # Проверка загрузки модели
    if MODEL is None:
        return {
            "status": "Ошибка",
            "content": "Модель распознавания речи не загружена"
        }

    try:
        audio = AudioSegment.from_file(BytesIO(data))
        text = decode_recording(
            model=MODEL, data=audio.export(format="wav").read())
        return {
            'status': 'success',
            'data': text
        }
    except Exception as e:
        logger.error(
            f"Error in decode_bytes endpoint: {str(e)}", exc_info=True)
        return {
            'status': 'error',
            'data': str(e)
        }


def decode_recording(model, data: bytes) -> str:
    """
    Расшифровка аудиозаписи с помощью модели Vosk
    :param model: Загруженная модель Vosk
    :param data: Аудиоданные в виде байтов
    :return: Словарь с результатом расшифровки
    """

    audio_file = BytesIO(data)
    wf = wave.open(audio_file, "rb")
    recognizer = KaldiRecognizer(model, wf.getframerate())
    result = ""

    while True:
        data = wf.readframes(32000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            partial_result = json.loads(recognizer.Result())
            if "text" in partial_result and partial_result["text"]:
                result += partial_result["text"] + " "

    final_result = json.loads(recognizer.FinalResult())
    if "text" in final_result and final_result["text"]:
        result += final_result["text"]

    wf.close()
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
