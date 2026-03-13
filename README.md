# insperjr-grupo01-backend

Backend em Flask para consulta de dados de supply chain da Ambev, conectado ao MongoDB Atlas.

## Pré-requisitos

- Python 3.10+
- Acesso ao banco MongoDB Atlas (credenciais no `.env`)

## Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repo>
cd insperjr-grupo01-backend

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Mac/Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env
cp .env.example .env
# Edite o .env com as credenciais do MongoDB Atlas
```

## Configuração (.env)

```
MONGO_URI=mongodb+srv://<usuario>:<senha>@cluster0.xgv12vm.mongodb.net/
DB_NAME=ambev
```

## Como rodar

```bash
python app.py
```

A API sobe em `http://localhost:5000`.

---

## Estrutura do projeto

```
insperjr-grupo01-backend/
├── app.py                    # inicia o servidor e registra as rotas
├── db.py                     # conexão com o MongoDB
├── routes/
│   ├── skus.py               # rotas de SKUs
│   ├── custos.py             # rotas de custos
│   ├── transferencias.py     # rotas de transferências
│   ├── producao_pcp.py       # rotas de produção PCP
│   ├── cenarios_semanais.py  # rotas de cenários semanais
│   └── cenario_atual_br.py   # rotas de cenário atual Brasil
├── .env                      # variáveis de ambiente (não versionado)
├── .env.example              # modelo do .env
├── requirements.txt
└── .gitignore
```

---

## Rotas da API

### SKUs — `/skus`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/skus` | Lista todos os SKUs |
| GET | `/skus?container_type=LONG NECK 355ML` | Filtra por tipo de embalagem |
| GET | `/skus/<sku_id>` | Retorna um SKU específico |

---

### Custos — `/custos`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/custos` | Lista todos os custos |
| GET | `/custos?sku_id=sku_goose_midway` | Filtra por SKU |
| GET | `/custos?tipo=transferencia` | Filtra por tipo (`transferencia`, `maco`, `producao`) |
| GET | `/custos/<sku_id>` | Todos os custos de um SKU |

---

### Transferências — `/transferencias`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/transferencias` | Lista todas as transferências |
| GET | `/transferencias?sku_id=sku_goose_midway` | Filtra por SKU |
| GET | `/transferencias?modal=Cabotagem` | Filtra por modal |
| GET | `/transferencias/<sku_id>` | Transferências de um SKU |

---

### Produção PCP — `/producao-pcp`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/producao-pcp` | Lista toda a produção |
| GET | `/producao-pcp?sku_id=sku_goose_midway` | Filtra por SKU |
| GET | `/producao-pcp?localidade=BR31` | Filtra por trecho do nome da fábrica |
| GET | `/producao-pcp/<sku_id>` | Produção de um SKU |

---

### Cenários Semanais — `/cenarios-semanais`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/cenarios-semanais` | Lista todos os cenários |
| GET | `/cenarios-semanais?sku_id=sku_goose_midway` | Filtra por SKU |
| GET | `/cenarios-semanais?cenario=Divulgado` | Filtra por cenário (`Divulgado`, `Nova_Demanda`) |
| GET | `/cenarios-semanais?geo_regiao=NE Norte` | Filtra por região |
| GET | `/cenarios-semanais/<sku_id>` | Cenários de um SKU |

---

### Cenário Atual BR — `/cenario-atual-br`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/cenario-atual-br` | Lista todos os cenários atuais |
| GET | `/cenario-atual-br?sku_id=sku_longneck_sk269` | Filtra por SKU |
| GET | `/cenario-atual-br?geo_regiao=SP` | Filtra por região (`SP`, `MG`, `RJ`, `SUL`, `CO`, `NENO`, `Export`, `TOTAL`) |
| GET | `/cenario-atual-br?is_total=true` | Retorna apenas o totalizador Brasil |
| GET | `/cenario-atual-br/<geo_regiao>` | Dados de uma região específica |
