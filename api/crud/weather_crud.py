from models.weather_model import Weather, session
from datetime import datetime
from sqlalchemy import and_


class WeatherCrud:
    def create_weather_log(city: str, temp: int, feels_like: int, description: str,
                           temp_min: int, temp_max: int, humidity: int, date: datetime):

        # Valida se há registro igual antes de gravar no banco de dados
        existing = session.query(Weather).filter(
            and_(
                Weather.city == city,
                Weather.date == date
            )
        ).first()

        if existing:
            return

        weather = Weather(city, temp, feels_like, description,
                          temp_min, temp_max, humidity, date)
        session.add(weather)
        session.commit()

        # Se for gravado, retorna o ID
        if weather.id:
            return weather.id
        else:
            return None
        
    def read_weather_logs(city: str = None, date: datetime = None):
        query = session.query(Weather)

        # Faz o filtro para achar correspondência de cidade e data
        if city:
            query = query.filter(Weather.city == city)
        if date:
            query = query.filter(Weather.date.between(
                datetime(date.year, date.month, date.day, 0, 0, 0),
                datetime(date.year, date.month, date.day, 23, 59, 59)
            ))

        listWeathers = query.all()

        return listWeathers

    def delete_weather_logs(city: str = None, date: datetime = None):
        query = session.query(Weather)

        if city:
            query = query.filter(Weather.city == city)
        if date:
            query = query.filter(Weather.date.between(
                datetime(date.year, date.month, date.day, 0, 0, 0),
                datetime(date.year, date.month, date.day, 23, 59, 59)
            ))

        deleted_count = query.delete()
        session.commit()

        # Retorna o número de exclusões executadas
        return deleted_count
