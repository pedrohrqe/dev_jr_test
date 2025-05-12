from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse, JSONResponse
from services.weather_service import WeatherService
from services.normalize_service import NormalizeService
from datetime import datetime
from pydantic import BaseModel
from typing import List

router = APIRouter()


# Definindo para que não apareça na documentação da FastAPI
@router.get("/", include_in_schema=False)
def root():
    # Definindo que ao entrar na raiz da api, seja exibida documentação
    return RedirectResponse(url="/docs")


class WeatherResponse(BaseModel):  # Definindo modelo de resposta do clima
    id: int = None
    city: str
    temp: int
    feels_like: int
    description: str
    temp_min: int
    temp_max: int
    humidity: int
    date: datetime


class deleteResponse(BaseModel):  # Definindo modelo de resposta para exclusão de clima
    deleted: bool
    qtd: int


@router.get("/weather", response_model=WeatherResponse)
def get_weather(city: str = Query(description="Cidade a ser consultado clima")):
    # Faz a validação se foi informada cidade
    if city and city.strip():
        try:
            weather = WeatherService.get_current_weather_service(city)

            weatherObj = WeatherResponse(
                id=weather["id"],
                city=weather["city"],
                temp=weather["temp"],
                feels_like=weather["feels_like"],
                description=weather["description"],
                temp_min=weather["temp_min"],
                temp_max=weather["temp_max"],
                humidity=weather["humidity"],
                date=weather["date"]
            )

            return weatherObj

        except Exception as e:
            # Caso haja erro, retorna 400 junto a mensagem de erro
            return JSONResponse(status_code=404, content={"error": str(e)})
    else:
        return JSONResponse(status_code=400, content={"error": "Informe uma cidade para consultar!"})


@router.get("/weather/history", response_model=List[WeatherResponse])
def get_weather_history(city: str = Query(None, description="Cidade a ser consultado clima"), date: str = Query(None, description="Data a ser consultado clima")):

    if not city and not date:
        return JSONResponse(status_code=404, content={"error": "Necessário cidade e/ ou data"})

    if date:
        date = NormalizeService.str_to_datetime(date)

    try:
        weather_data = WeatherService.read_weather_service(city, date)

        weathers = [
            WeatherResponse(
                id=weather.id,
                city=weather.city,
                temp=weather.temp,
                feels_like=weather.feels_like,
                description=weather.description,
                temp_min=weather.temp_min,
                temp_max=weather.temp_max,
                humidity=weather.humidity,
                date=weather.date
            )
            for weather in weather_data
        ]

        return weathers

    except Exception as e:
        return JSONResponse(status_code=404, content={"error": str(e)})


@router.delete("/weather/history", response_model=deleteResponse)
def delete_weather_history(city: str = Query(None, description="Nome da cidade para deletar os dados"), date: str = Query(None, description="Nome da cidade para deletar os dados")):

    if date:
        date = NormalizeService.str_to_datetime(date)

    try:
        delete = WeatherService.delete_Weather_service(city, date)

        return deleteResponse(
            deleted=True,
            qtd=delete
        )

    except Exception as e:
        return JSONResponse(status_code=404, content={"error": str(e)})
