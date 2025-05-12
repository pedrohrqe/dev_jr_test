from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_SQLLITE_HOST
from datetime import datetime

# criando banco de dados ou conectando caso já exista
db = create_engine(DB_SQLLITE_HOST)

# Criando objeto da sessão
Session = sessionmaker(bind=db)
# Instanciando a sessão
session = Session()

Base = declarative_base()


class Weather(Base):
    # Nomeando a tabela a ser usada/ criada
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, index=True)
    temp = Column(Integer)
    feels_like = Column(Integer)
    description = Column(String)
    temp_min = Column(String)
    temp_min = Column(Integer)
    temp_max = Column(Integer)
    humidity = Column(Integer)
    date = Column(DateTime)

    # Usando a classe construtora
    def __init__(self, city, temp, feels_like, description, temp_min, temp_max, humidity, date=datetime.now()):
        self.city = city
        self.temp = temp
        self.feels_like = feels_like
        self.description = description
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.humidity = humidity
        self.date = date


Base.metadata.create_all(bind=db)