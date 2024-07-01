from fastapi import FastAPI, Request

from services import get_city_from_ip, get_temperature_for_city, get_client_ip, parse_quoted_text

app = FastAPI()


@app.get("/api/hello")
async def say_hello(request: Request):
    visitor_name = await parse_quoted_text(request.query_params.get("visitor_name", ""))
    ip_address = await get_client_ip(request)
    city = await get_city_from_ip(ip_address)
    temperature = await get_temperature_for_city(city)
    return {
        "client_ip": ip_address,
        "location": city,
        "greeting": f"Hello{f' {visitor_name}' if visitor_name else visitor_name}!,"
                    f" the temperature is {temperature} in {city}"
    }
