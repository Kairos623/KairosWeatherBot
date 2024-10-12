import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram import F
import asyncio

telegram_bot_token = '8008583492:AAHJrj4dAUNPVC26ybF0pV3KsEsLrqU408k'
openweather_api_key = '248f4bcacf83f93bd9e6a5ca199c8384'

bot = Bot(token=telegram_bot_token)
dp = Dispatcher()


async def get_weather(city_name):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': openweather_api_key,
        'units': 'metric',
        'lang': 'ru'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params, timeout=5) as response:
                if response.status == 404:
                    error_data = await response.json()
                    return f"Город не найден. Пожалуйста, проверьте название."

                response.raise_for_status()
                data = await response.json()

                city = data['name']
                temp = round(data['main']['temp'])
                humidity = data['main']['humidity']
                weather_description = data['weather'][0]['description']

                return (f"Погода в городе {city}:\n"
                        f"Температура: {temp}°C\n"
                        f"Влажность: {humidity}%\n"
                        f"Описание: {weather_description.capitalize()}")

    except asyncio.TimeoutError:
        return "Превышено время ожидания ответа от сервера или сервер в данный момент недоступен. Попробуйте снова."
    except aiohttp.ClientError as e:
        return f"Ошибка при получении данных: {e}"


@dp.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь мне название города, чтобы узнать погоду.")


@dp.message()
async def send_weather(message: Message):
    city_name = message.text
    weather_info = await get_weather(city_name)
    await message.answer(weather_info)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())