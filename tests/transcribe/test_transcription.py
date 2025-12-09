from pathlib import Path

import requests

# Путь к тестовому аудиофайлу
TEST_AUDIO_PATH = Path(__file__).parent / "rap.wav"

# URL сервиса
BASE_URL = "http://localhost:8300"


def test_decode_file_endpoint():
    """Тестирование эндпоинта /decode/file."""
    # Открываем файл и отправляем запрос
    with open(TEST_AUDIO_PATH, "rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        response = requests.post(
            f"{BASE_URL}/decode/file", files=files, timeout=120)

    # Проверяем статус ответа
    assert response.status_code == 200

    # Проверяем структуру ответа
    data = response.json()
    assert "status" in data
    assert "data" in data
    assert 'все' in data['data']

    # Проверяем, что статус не "error"
    assert data["status"] != "error"


def test_decode_bytes_endpoint():
    """Тестирование эндпоинта /decode/bytes."""
    # Читаем байты аудиофайла
    with open(TEST_AUDIO_PATH, "rb") as f:
        audio_bytes = f.read()

    # Отправляем запрос с байтами
    response = requests.post(
        f"{BASE_URL}/decode/bytes",
        data=audio_bytes,
        headers={"Content-Type": "application/octet-stream",

                 }, timeout=20
    )

    # Проверяем статус ответа
    print(response.text)
    assert response.status_code == 200

    # Проверяем структуру ответа
    data = response.json()
    print(data)

    assert "status" in data
    assert "data" in data

    # Проверяем, что статус не "error"
    assert data["status"] != "error", f"Ошибка при расшифровке: {data['data']}"


def test_decode_file_endpoint_no_file():
    """Тестирование эндпоинта /decode/file без файла."""
    response = requests.post(f"{BASE_URL}/decode/file", timeout=5)
    assert response.status_code == 422  # Unprocessable Entity


def test_decode_bytes_endpoint_no_data():
    """Тестирование эндпоинта /decode/bytes без данных."""
    response = requests.post(f"{BASE_URL}/decode/bytes", timeout=5)
    assert response.status_code == 422  # Unprocessable Entity


def test_root_endpoint():
    """Тестирование корневого эндпоинта."""
    response = requests.get(f"{BASE_URL}/", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Audio Transcription Service is running"
