import unicodedata
from datetime import datetime


class NormalizeService:
    # Função para normalizar o texto, deixando em maíusculo e sem acentos
    def normalize_text(texto: str) -> str:
        texto_sem_acentos = unicodedata.normalize(
            'NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        texto_formatado = texto_sem_acentos.upper()
        return texto_formatado

    def str_to_datetime(data_str: str, formato: str = "%Y-%m-%d") -> datetime:
        return datetime.strptime(data_str, formato)

