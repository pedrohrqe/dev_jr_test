import requests
from datetime import datetime
from config import API_KEY, API_BASE_URL_WEATHER, API_BASE_URL_FOREACH
from crud.weather_crud import WeatherCrud
from services.normalize_service import NormalizeService


class WeatherService:
    def get_current_weather_service(city: str) -> dict:
        # Parametros para consulta, clima atual
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "pt_br"
        }

        response = requests.get(API_BASE_URL_WEATHER, params=params)

        # Se não for obtido retorno, é voltada exceção e interrompido fluxo
        if response.status_code != 200:
            raise Exception("Erro ao consultar clima da cidade informada!")

        # Convertido valores para json
        data = response.json()

        # Montagem do objeto para gravação no bd e exibição
        weather_data = {
            "city": NormalizeService.normalize_text(data["name"]),
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "description": data["weather"][0]["description"],
            "temp_min": round(data["main"]["temp_min"]),
            "temp_max": round(data["main"]["temp_max"]),
            "humidity": data["main"]["humidity"],
            "date": datetime.now()
        }

        # Realizada a gravação no banco de dados
        newWeather = WeatherCrud.create_weather_log(
            weather_data["city"],
            weather_data["temp"],
            weather_data["feels_like"],
            weather_data["description"],
            weather_data["temp_min"],
            weather_data["temp_max"],
            weather_data["humidity"],
            weather_data["date"]
        )

        # Obntém id e insere nas informações atuais pra exibição
        weather_data["id"] = newWeather

        return weather_data

    def get_weather_history_service(city: str) -> dict:
        # Parametros para consulta, clima de 5 dias, 3 em 3 horas
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "pt_br"
        }

        response = requests.get(API_BASE_URL_FOREACH, params=params)

        # Se não for obtido retorno, é voltada exceção e interrompido fluxo
        if response.status_code != 200:
            raise Exception("Erro ao consultar clima da cidade informada!")

        data = response.json()

        # Extraindo a chave list do  response
        list_weathers = data["list"]
        new_list_weathers = []

        # Estabelecido cidade fora do loop pois é igual, para evitar processamento repetido
        city = NormalizeService.normalize_text(data["city"]["name"])

        # Percorre a lista com os dados climáticos das horas/ dia e insere no banco de dados
        for weather in list_weathers:
            w = {
                "city": city,
                "temp": round(weather["main"]["temp"]),
                "feels_like": round(weather["main"]["feels_like"]),
                "description": weather["weather"][0]["description"],
                "temp_min": round(weather["main"]["temp_min"]),
                "temp_max": round(weather["main"]["temp_max"]),
                "humidity": round(weather["main"]["humidity"]),
                "date": datetime.strptime(weather["dt_txt"], "%Y-%m-%d %H:%M:%S")
            }

            # Cria o registro com o dado climático obtido
            WeatherCrud.create_weather_log(
                w["city"],
                w["temp"],
                w["feels_like"],
                w["description"],
                w["temp_min"],
                w["temp_max"],
                w["humidity"],
                w["date"]
            )

            new_list_weathers.append(w)

        # Retorna o objeto com os dados climáticos
        return new_list_weathers

    def read_weather_service(city: str = None, date: datetime = None) -> dict:
        # Se houver cidade, faz a normalização do texto para facilitar a busca pelos dados e tenta obter o clima dos dias para cidade
        if city:
            # Acionado a validação de clima dos dias para armazenar as informações para consulta
            try:
                WeatherService.get_weather_history_service(city)
            except Exception as e:
                print(f"Erro ao buscar dados da cidade '{city}': {e}")

            weathers = WeatherCrud.read_weather_logs(
                NormalizeService.normalize_text(city), date)
        else:
            weathers = WeatherCrud.read_weather_logs(city, date)

        # Se não forem encontrados registros, retorna exceção
        if not weathers:
            raise Exception("Nenhum registro encontrado.")

        return weathers

    def delete_Weather_service(city: str = None, date: datetime = None) -> int:
        # Validação para só executar caso haja cidade ou data
        if not city and not date:
            raise Exception("Necessário informar cidade ou data!")

        if city:
            # Executa a remoção do banco de dados
            deleted_count = WeatherCrud.delete_weather_logs(
                NormalizeService.normalize_text(city), date)
        else:
            deleted_count = WeatherCrud.delete_weather_logs(city, date)
        # Se houver exclusões, retorna quantas houveram, se não retorna exceção
        if deleted_count > 0:
            return deleted_count
        else:
            raise Exception("Nenhum registro encontrado para deletar.")
