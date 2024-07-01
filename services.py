import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException, Request

load_dotenv()


async def parse_quoted_text(text: str) -> str:
    return text.strip('"').strip("'")


async def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]


async def get_city_from_ip(ip_address: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://ipinfo.io/{ip_address}")
        response_data = response.json()
        return response_data.get("city", "Unknown")


async def get_temperature_for_city(city: str) -> str:
    url = os.environ.get("OWM_URL", "https://api.openweathermap.org/data/2.5/weather")
    temp_unit = os.environ.get("TEMP_UNIT", "metric")
    params = {
        "q": city,
        "appid": os.environ.get("OWM_API_KEY"),
        "units": temp_unit
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="An error occurred")

        data = response.json()
        temperature = data["main"]["temp"]
        unit_name = await get_temperature_unit_name(temp_unit)
        return f"{temperature} degree {unit_name}"


async def get_temperature_unit_name(unit: str) -> str:
    units = {
        "metric": "Celsius",
        "imperial": "Fahrenheit"
    }
    return units.get(unit, "")
