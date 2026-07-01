import requests
import json

def get_weather(city_name, api_key):
    """
    Функция для получения данных о погоде с OpenWeatherMap.
    """
    # Формируем URL запроса с параметрами
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric',  # Для получения температуры в Цельсиях
        'lang': 'ru'        # Для описаний погоды на русском
    }

    try:
        # Отправляем GET-запрос
        response = requests.get(base_url, params=params)
        # Проверяем код статуса ответа
        response.raise_for_status()

        # Декодируем JSON-ответ
        weather_data = response.json()

        # Проверяем, нет ли ошибки в ответе API (например, город не найден)
        if weather_data.get('cod') != 200:
            print(f"Ошибка API: {weather_data.get('message', 'Неизвестная ошибка')}")
            return None

        return weather_data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Ошибка соединения: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Таймаут запроса: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка запроса: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Ошибка разбора JSON: {json_err}")
    return None

def print_weather(weather_data):
    """
    Функция для структурированного вывода погодных данных.
    """
    if not weather_data:
        print("Нет данных для вывода.")
        return

    # Извлекаем нужные данные из сложной структуры JSON
    city = weather_data.get('name', 'N/A')
    country = weather_data.get('sys', {}).get('country', 'N/A')
    temp = weather_data.get('main', {}).get('temp', 'N/A')
    feels_like = weather_data.get('main', {}).get('feels_like', 'N/A')
    humidity = weather_data.get('main', {}).get('humidity', 'N/A')
    pressure = weather_data.get('main', {}).get('pressure', 'N/A')
    weather_desc = weather_data['weather'][0]['description'] if weather_data.get('weather') else 'N/A'
    wind_speed = weather_data.get('wind', {}).get('speed', 'N/A')

    # Форматированный вывод
    print("\n" + "="*40)
    print(f"ПОГОДА В {city.upper()}, {country}")
    print("="*40)
    print(f"🌡  Температура:      {temp} °C")
    print(f"🥶 Ощущается как:    {feels_like} °C")
    print(f"💧 Влажность:        {humidity} %")
    print(f"🌀 Давление:         {pressure} гПа")
    print(f"🌤  Описание:         {weather_desc.capitalize()}")
    print(f"💨 Скорость ветра:   {wind_speed} м/с")
    print("="*40)

# ======== ИСПОЛНЯЕМЫЙ КОД ========
if __name__ == "__main__":
    # Конфигурация (поместите сюда ваш ключ)
    API_KEY = "86ed401ff85894f61e060884b0e19564"  
    CITY_NAME = "Tokyo"  

    print(f"Запрашиваю данные о погоде для города: {CITY_NAME}...")
    data = get_weather(CITY_NAME, API_KEY)

    if data:
        print_weather(data)
        # (Опционально) Сохраним полный ответ в файл для изучения
        with open('weather_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("\nПолные данные сохранены в файл 'weather_data.json'")