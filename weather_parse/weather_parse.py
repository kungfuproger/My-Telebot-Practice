def weather():
    import requests

    lat = 45.035789
    lon = 38.918836

    params = {
        "lat": lat,
        "lon": lon,
        "lang": "ru_RU",
        "limit": 1,  # срок прогноза в днях
        "hours": True,  # наличие почасового прогноза
        "extra": False,  # подробный прогноз осадков
    }

    api_key = "cdd4c78d-37ba-457b-8b30-c1bc32546f92"

    url = "https://api.weather.yandex.ru/v2/forecast"

    response = requests.get(
        url, params=params, headers={"X-Yandex-API-Key": api_key}
    )

    if response.status_code == 200:
        data = response.json()
        weather_dict = {
            "Температура воздуха °C": {data["fact"]["temp"]},
            "Ощущается как °C": {data["fact"]["feels_like"]},
            "Скорость ветра м/с": {data["fact"]["wind_speed"]},
            "Давление мм рт. ст.": {data["fact"]["pressure_mm"]},
            "Влажность %": {data["fact"]["humidity"]},
            "Погодное описание": {data["fact"]["condition"]},
        }
        text = (
            f'Температура воздуха: {data["fact"]["temp"]} °C\n'
            f'Ощущается как: {data["fact"]["feels_like"]} °C\n'
            f'Скорость ветра: {data["fact"]["wind_speed"]} м/с\n'
            f'Давление: {data["fact"]["pressure_mm"]} мм рт. ст.\n'
            f'Влажность: {data["fact"]["humidity"]} %\n'
            f'Погодное описание: {data["fact"]["condition"]}\n'
        )
        print(text)
    else:
        print(f"Ошибка: {response.status_code}")

    return weather_dict, text


if __name__ == "__main__":
    weather()
