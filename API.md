# API REST – Dashboard Executivo Ambev

Base URL: `http://localhost:5000/api/v1`

Database MongoDB: **ambev**  
Coleções (espelhando a pasta `data/`): `skus`, `cenario_atual_br`, `cenarios_semanais`, `custos`, `producao_pcp`, `transferencias`.

---

## Resposta padronizada (listas)

Todas as listas retornam:

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

Parâmetros opcionais comuns:

| Parâmetro  | Descrição                    | Exemplo        |
|-----------|-------------------------------|----------------|
| `page`    | Página (default 1)           | `?page=2`      |
| `per_page`| Itens por página (máx. 500)  | `?per_page=10` |
| `sort`    | Ordenação (recurso-dependente) | `?sort=nome`  |
| `order`   | `asc` ou `desc`              | `?order=desc`  |
| `fields`  | Campos desejados (separados por vírgula) | `?fields=_id,nome,codigo` |

---

## Endpoints

### Dashboard (uma chamada para o front)

- **GET /api/v1/dashboard**  
  Resumo: contagens por coleção, totais Brasil (cenário atual), lista de SKUs e regiões.  
  Query: `?incluir_skus=true` (default) para incluir lista de SKUs.

### SKUs

- **GET /api/v1/skus**  
  Filtros: `container_type`, `codigo`. Ordenação: `codigo`, `nome`, `container_type`, `unidade_volume`.
- **GET /api/v1/skus/<sku_id>**  
  Um SKU por `_id`.

### Cenário atual Brasil

- **GET /api/v1/cenario-atual-br**  
  Filtros: `sku_id`, `geo_regiao`, `is_total` (true/false).
- **GET /api/v1/cenario-atual-br/<geo_regiao>**  
  Ex.: `/cenario-atual-br/SP`, `/cenario-atual-br/TOTAL`.

### Cenários semanais

- **GET /api/v1/cenarios-semanais**  
  Filtros: `sku_id`, `cenario`, `geo_regiao`.
- **GET /api/v1/cenarios-semanais/<sku_id>**  
  Cenários de um SKU.

### Custos

- **GET /api/v1/custos**  
  Filtros: `sku_id`, `tipo`, `origem`, `destino`.
- **GET /api/v1/custos/<sku_id>**  
  Custos de um SKU (lista paginada).

### Produção PCP

- **GET /api/v1/producao-pcp**  
  Filtros: `sku_id`, `localidade`, `linha`.
- **GET /api/v1/producao-pcp/<sku_id>**  
  Produção por SKU.

### Transferências

- **GET /api/v1/transferencias**  
  Filtros: `sku_id`, `modal`, `destino_geo`.
- **GET /api/v1/transferencias/<sku_id>**  
  Transferências de um SKU.

---

## Popular o banco (seed)

Com MongoDB rodando e variável `DB_NAME=ambev` (ou default):

```bash
python -m scripts.seed_ambev
```

Os arquivos em `data/` são mapeados para as coleções de mesmo nome; `custos (1).json` é carregado na coleção `custos`.
