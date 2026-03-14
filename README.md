# insperjr-grupo01-backend

API REST em Flask para o **Dashboard Executivo Ambev**: consulta de dados de supply chain (SKUs, cenários, custos, produção PCP, transferências). Conectada ao MongoDB (database `ambev`).

---

## Pré-requisitos

- **Python 3.10+**
- **MongoDB** (local em `localhost:27017` ou Atlas — URI no `.env`)

---

## Instalação

```bash
# 1. Clone e entre na pasta
git clone <url-do-repo>
cd insperjr-grupo01-backend

# 2. Ambiente virtual (recomendado)
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Mac/Linux

# 3. Dependências
pip install -r requirements.txt

# 4. Variáveis de ambiente
cp .env.example .env
# Edite .env com MONGO_URI, DB_NAME e FRONTEND_URL (veja abaixo)
```

---

## Configuração (`.env`)

| Variável       | Descrição                          | Exemplo |
|----------------|------------------------------------|---------|
| `MONGO_URI`    | URI do MongoDB                     | `mongodb://localhost:27017` ou URI Atlas |
| `DB_NAME`      | Nome do database                   | `ambev` |
| `FRONTEND_URL` | Origem permitida pelo CORS (sem barra no final) | `http://localhost:5173` |

**CORS:** Use exatamente a URL do front (ex.: Vite = `http://localhost:5173`). Não coloque barra no final, senão o navegador bloqueia por CORS.

---

## Como rodar

```bash
python app.py
```

A API sobe em **http://localhost:5000**. A raiz `http://localhost:5000/` retorna um JSON com nome da API e lista de recursos.

---

## Popular o banco (seed)

Os dados iniciais ficam em arquivos JSON na pasta **`data/`**. Cada arquivo corresponde a uma coleção no MongoDB:

| Arquivo em `data/`     | Coleção no MongoDB   |
|------------------------|----------------------|
| `skus.json`            | `skus`               |
| `cenario_atual_br.json`| `cenario_atual_br`   |
| `cenarios_semanais.json` | `cenarios_semanais` |
| `custos (1).json`      | `custos`             |
| `producao_pcp.json`    | `producao_pcp`       |
| `transferencias.json`  | `transferencias`     |

Com o MongoDB rodando:

```bash
python -m scripts.seed_ambev
```

O script faz upsert por `_id`, então pode ser executado mais de uma vez.

---

## Estrutura do projeto

```
insperjr-grupo01-backend/
├── app.py                 # Entrada: Flask, CORS, registro de rotas
├── db.py                  # Conexão MongoDB (ambev) e serialize_doc
├── requirements.txt
├── Procfile               # Deploy: gunicorn (Heroku, Railway, Render)
├── runtime.txt            # Python 3.11 (Heroku)
├── Dockerfile             # Deploy em container (waitress)
├── .dockerignore
├── .env                   # Variáveis de ambiente (não versionado)
├── .env.example
├── API.md                 # Documentação detalhada dos endpoints
├── data/                  # JSONs para seed (um por coleção)
├── routes/
│   ├── skus.py
│   ├── custos.py
│   ├── transferencias.py
│   ├── producao_pcp.py
│   ├── cenarios_semanais.py
│   ├── cenario_atual_br.py
│   └── dashboard.py       # GET /api/v1/dashboard (resumo para o front)
├── utils/
│   └── rest.py            # Paginação, ordenação, fields, resposta data+meta
├── scripts/
│   └── seed_ambev.py      # Popula MongoDB a partir de data/
└── tests/
    └── test_routes.py     # Testes contra os JSON em data/
```

---

## API — Base URL e formato

- **Base URL:** `http://localhost:5000/api/v1`

**Listas** retornam:

```json
{
  "data": [ ... ],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
  }
}
```

Parâmetros opcionais: `?page=1&per_page=20&sort=nome&order=asc&fields=_id,nome,codigo` (conforme recurso).

**Recurso único** (ex.: GET `/api/v1/skus/<id>`): retorna o objeto direto ou `404` com `{"error": "Recurso não encontrado"}`.

---

## Rotas (resumo)

| Recurso | GET lista | GET por ID / filtro |
|---------|-----------|----------------------|
| **Dashboard** | `/api/v1/dashboard?incluir_skus=true` — contagens, totais Brasil, SKUs, regiões | — |
| **SKUs** | `/api/v1/skus` — filtros: `container_type`, `codigo` | `/api/v1/skus/<sku_id>` |
| **Cenário atual BR** | `/api/v1/cenario-atual-br` — filtros: `sku_id`, `geo_regiao`, `is_total` | `/api/v1/cenario-atual-br/<geo_regiao>` |
| **Cenários semanais** | `/api/v1/cenarios-semanais` — filtros: `sku_id`, `cenario`, `geo_regiao` | `/api/v1/cenarios-semanais/<sku_id>` |
| **Custos** | `/api/v1/custos` — filtros: `sku_id`, `tipo`, `origem`, `destino` | `/api/v1/custos/<sku_id>` |
| **Produção PCP** | `/api/v1/producao-pcp` — filtros: `sku_id`, `localidade`, `linha` | `/api/v1/producao-pcp/<sku_id>` |
| **Transferências** | `/api/v1/transferencias` — filtros: `sku_id`, `modal`, `destino_geo` | `/api/v1/transferencias/<sku_id>` |

Detalhes (filtros, campos, exemplos): ver **`API.md`**.

---

## Testes

Com o MongoDB populado (`python -m scripts.seed_ambev`):

```bash
python tests/test_routes.py
```

Os testes validam listas, totais e filtros contra os JSON em `data/`.

---

## Verificar e liberar portas (Windows)

Se a API não sobe ou o front dá "connection refused", pode haver outro processo na porta.

**Ver o que usa a porta 5000:**

```bash
netstat -ano | findstr :5000
```

A última coluna é o **PID**. Para encerrar:

```bash
taskkill /PID <número> /F
```

Substitua `5000` por `8000` (ou outra porta) se o backend estiver configurado para ela.

---

## Deploy

### Variáveis de ambiente (obrigatórias em produção)

| Variável       | Descrição |
|----------------|-----------|
| `MONGO_URI`    | URI do MongoDB (ex.: `mongodb+srv://user:pass@cluster.mongodb.net/`) |
| `DB_NAME`      | `ambev` |
| `FRONTEND_URL` | URL do frontend (sem barra no final). Várias origens: `https://app.com,https://www.app.com` |

A maioria das plataformas define `PORT` automaticamente. Opcional: `FLASK_ENV=production`.

### Deploy com Procfile (Heroku, Railway, Render)

O repositório já inclui um `Procfile`. A plataforma usa `gunicorn` e a variável `PORT`:

```bash
# Exemplo: após conectar o repositório, configure no painel:
# MONGO_URI=...
# DB_NAME=ambev
# FRONTEND_URL=https://seu-front.vercel.app
```

Para **Heroku**, use `runtime.txt` (Python 3.11). O build instala as dependências e sobe com `web: gunicorn --bind 0.0.0.0:$PORT app:app`.

### Deploy com Docker (Railway, Render, Fly.io, etc.)

```bash
docker build -t ambev-backend .
docker run -p 5000:5000 -e MONGO_URI=... -e DB_NAME=ambev -e FRONTEND_URL=... ambev-backend
```

Na plataforma, aponte o serviço para este Dockerfile e configure as variáveis de ambiente. O container usa `python app.py` com **waitress** e lê `PORT` do ambiente (padrão 5000).

### Rodar em produção local (waitress)

Com `PORT` ou `FLASK_ENV=production` definidos, `python app.py` sobe com waitress em `0.0.0.0:PORT`:

```bash
# Windows
set PORT=8000
set FLASK_ENV=production
python app.py

# Linux/Mac
export PORT=8000 FLASK_ENV=production
python app.py
```
