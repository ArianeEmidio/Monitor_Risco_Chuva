# ================================
# IMPORTAÇÕES
# ================================

# FastAPI é o framework que cria a API
from fastapi import FastAPI, HTTPException

# requests permite fazer requisições HTTP para APIs externas
import requests


# ================================
# CRIAÇÃO DA APLICAÇÃO
# ================================

# Criando a aplicação web
app = FastAPI()

# ============================================
# CONFIGURAÇÃO DE CORS (Cross-Origin Resource Sharing)
# ============================================

# Importei o middleware responsável por controlar quem pode acessar nossa API a partir do navegador.
from fastapi.middleware.cors import CORSMiddleware

# Adicionando um "middleware" à aplicação.
# Middleware é algo que intercepta requisições antes de chegarem nas rotas.
app.add_middleware(
    CORSMiddleware,

    # allow_origins define quais origens podem acessar a API.
    # "*" significa: qualquer origem pode acessar.
    # Isso é aceitável em ambiente de desenvolvimento.
    # Em produção não é recomendado usar "*".
    allow_origins=["*"],

    # Permite envio de cookies/autenticação se necessário.
    allow_credentials=True,

    # Permite todos os métodos HTTP (GET, POST, PUT, DELETE etc).
    allow_methods=["*"],

    # Permite todos os cabeçalhos na requisição.
    allow_headers=["*"],
)

# ================================
# ROTA INICIAL (TESTE)
# ================================

# Quando alguém acessar: http://127.0.0.1:8000/
# Essa função será executada
@app.get("/")
def home():
    return {
        "mensagem": "API de Monitoramento de RISCO - DESASTRES NATURAIS"
    }


# ================================
# FUNÇÃO 1 - CONVERTER CIDADE EM COORDENADAS
# ================================

def geocode_city(city: str):

    # URL da API de Geocoding (converte nome -> latitude/longitude)
    url = "https://geocoding-api.open-meteo.com/v1/search"

         # Parâmetros enviados para a API
         # Eles serão transformados em:
         # ?name=...&count=...&language=...&format=...
    params = {
        "name": city,        # Nome da cidade digitada pelo usuário
        "count": 1,          # Retornar apenas o melhor resultado
        "language": "pt",    # Resposta em português
        "format": "json",    # Queremos resposta em formato JSON
    }

    # Faz a requisição para a API externa
    response = requests.get(url, params=params, timeout=10)

    # Se a API retornar erro (404, 500, etc.), interrompe aqui
    response.raise_for_status()

    # Converte a resposta JSON (texto) em dicionário Python
    data = response.json()

    # Pega a lista de resultados
    results = data.get("results")

    # Se não houver resultado, retorna None
    if not results:
        return None

    # Pega o primeiro resultado da lista
    best = results[0]

    # Extrai os campos separadamente
    nome = best.get("name", "")
    estado = best.get("admin1", "")
    pais = best.get("country", "")

    # Monto a string completa
    texto = f"{nome}, {estado}, {pais}"

    # Removendo vírgulas e espaços extras no começo/fim
    texto_limpo = texto.strip(", ")

    # Retornar um dicionário organizado
    return {
        "name": texto_limpo,
        "latitude": best["latitude"],
        "longitude": best["longitude"],
    }


# ================================
# FUNÇÃO 2 - PEGAR CHUVA ATUAL
# ================================

def get_precipitation_now(latitude: float, longitude: float):

    # URL da API de previsão do tempo
    url = "https://api.open-meteo.com/v1/forecast"

    # Parâmetros enviados
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "precipitation,rain,showers",
        "timezone": "America/Sao_Paulo",
    }

    # Faz requisição para a API
    response = requests.get(url, params=params, timeout=10)

    # Interrompe se houver erro HTTP
    response.raise_for_status()

    # Converte JSON para dicionário
    data = response.json()

    # Pega o bloco "current"
    current_data = data.get("current", {})

    # Pega o valor de precipitação
    precip = current_data.get("precipitation", 0.0)

    return float(precip or 0.0)


# ================================
# FUNÇÃO 3 - CLASSIFICAR RISCO
# ================================

def classify_risk(precip_mm: float):

    # Regra simples de classificação
    if precip_mm > 10:
        return "ALTO"

    if precip_mm >= 2:
        return "MÉDIO"

    return "BAIXO"


# ================================
# ROTA PRINCIPAL - /risco
# ================================

@app.get("/risco")
def risco(cidade: str):

    print(f"[1] Cidade recebida: {cidade}")

    # 1) Converter cidade em coordenadas
    loc = geocode_city(cidade)

    print(f"[2] Resultado do geocoding: {loc}")

    # Se cidade não for encontrada
    if not loc:
        raise HTTPException(status_code=404, detail="Cidade não encontrada")

    # 2) Buscar chuva atual
    chuva_mm = get_precipitation_now(loc["latitude"], loc["longitude"])

    print(f"[3] Chuva atual (mm): {chuva_mm}")

    # 3) Classificar risco
    nivel = classify_risk(chuva_mm)

    print(f"[4] Nível de risco: {nivel}")

    # 4) Retornar resposta final
    return {
        "cidade_pesquisada": cidade,
        "local_encontrado": loc["name"],
        "latitude": loc["latitude"],
        "longitude": loc["longitude"],
        "precipitacao_mm": chuva_mm,
        "nivel_risco": nivel,
    }