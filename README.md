# 🌦️ WeatherAPI - API de Clima

## 📌 Sobre o projeto
Este projeto é uma **API REST** desenvolvida em **Python** com **FastAPI**, permitindo a consulta do **clima atual** de qualquer cidade, bem como o acesso ao **histórico de clima**, com filtros opcionais por cidade e/ou data.

Além de ser uma aplicação funcional, também serve como estudo prático de integração com serviços externos (OpenWeatherMap), manipulação de banco de dados e boas práticas com FastAPI.

---

## 🛠️ Tecnologias Utilizadas
- Python 3.13
- FastAPI
- SQLite
- SQLAlchemy
- OpenWeatherMap (API externa de clima)
- Git

---

## 🔗 Endpoints da API

| Método | Rota               | Parâmetros                           | Descrição |
|--------|--------------------|--------------------------------------|-----------|
| GET    | `/`                | Nenhum                               | Exibe a documentação do projeto |
| GET    | `/weather`         | `city` (obrigatório)                 | Retorna o clima atual da cidade informada |
| GET    | `/weather/history` | `city` (opcional), `date` (opcional) | Retorna o histórico de clima com base na cidade e/ou data |
| DELETE | `/weather/history` | `city` ou `date` (ao menos um)       | Remove registros climáticos com base na cidade e/ou data |

---

## 📁 Estrutura do Projeto

    │   meubanco.db
    │   readme.md
    │   requirements.txt
    │
    └───app
        │   config.py
        │   main.py
        │
        ├───crud
        │       weather_crud.py
        │
        ├───models
        │       weather_model.py
        │
        ├───routers
        │       weather.py
        │
        └───services
                normalize_service.py
                weather_service.py


## ▶️ Como Executar o Projeto

Você pode optar por acessar a api hospedada no Render, [clicando aqui.](https://test-dev-junior-use.onrender.com)

### 1. **Clone o repositório:**
```bash
git clone https://github.com/pedrohrqe/dev_jr_test.git
cd dev_jr_test
```

### 2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

### 3. **Execute a aplicação:**
```bash
python -m app.main
```
ou
```bash
uvicorn app.main:app --reload
```