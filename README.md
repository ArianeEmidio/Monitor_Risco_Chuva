# 🌧️ Monitor de Risco por Chuva

Aplicação web cliente-servidor desenvolvida com **FastAPI** e **JavaScript**, que consulta dados climáticos em tempo real para classificar o nível de risco com base na precipitação atual da cidade informada.

O sistema integra APIs públicas para:

- 📍 Conversão de cidade em coordenadas geográficas
- 🌦️ Consulta de precipitação atual
- ⚠️ Classificação de risco (Baixo, Médio, Alto)

---

## 🚀 Tecnologias Utilizadas

- Python
- FastAPI
- JavaScript (Fetch API)
- HTML
- Git & GitHub

---

## 🧠 Arquitetura

O projeto segue uma estrutura simples de aplicação REST:


Frontend (HTML + JS)
↓
FastAPI (Backend REST)
↓
APIs externas (Geocodificação + Clima)


---

## ⚙️ Como Executar Localmente

1️⃣ Clone o repositório:

```bash
git clone https://github.com/ArianeEmidio/Monitor_Risco_Chuva.git

2️⃣ Acesse a pasta:

cd Monitor_Risco_Chuva

3️⃣ Crie e ative o ambiente virtual:

python -m venv .venv
.venv\Scripts\activate

4️⃣ Instale as dependências:

pip install -r requirements.txt

5️⃣ Execute o servidor:

uvicorn app.main:app --reload

6️⃣ Abra o arquivo index.html no navegador.

🔎 Endpoint Principal
GET /risco?cidade=NomeDaCidade

Exemplo:

http://127.0.0.1:8000/risco?cidade=Juiz%20de%20Fora

📌 Funcionalidades

✔ Conversão automática de cidade para coordenadas
✔ Consulta de precipitação atual
✔ Classificação automática de risco
✔ Interface simples e intuitiva
✔ Estrutura organizada para futura expansão

📈 Em Breve:

✔ Deploy em nuvem (Render / Railway)

✔ Interface estilizada com CSS avançado

✔ Histórico de consultas

✔ Dashboard com gráficos

👩‍💻 Sobre o Projeto

    Projeto desenvolvido com foco em prática de:

    ➜ Integração com APIs externas

    ➜ Arquitetura cliente-servidor

    ➜ Versionamento com Git

    ➜ Estruturação de backend com FastAPI
