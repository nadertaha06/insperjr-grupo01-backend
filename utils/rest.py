"""
Utilitários REST: paginação, seleção de campos, ordenação e resposta padronizada.
Uso no dashboard executivo com menos requisições e payloads controlados.
"""
from flask import request, jsonify


# Limites padrão para dashboard (evitar payloads gigantes)
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 50
MAX_PER_PAGE = 500


def parse_pagination():
    """Lê page e per_page da query string."""
    try:
        page = max(1, int(request.args.get("page", DEFAULT_PAGE)))
    except (TypeError, ValueError):
        page = DEFAULT_PAGE
    try:
        per_page = min(MAX_PER_PAGE, max(1, int(request.args.get("per_page", DEFAULT_PER_PAGE))))
    except (TypeError, ValueError):
        per_page = DEFAULT_PER_PAGE
    return page, per_page


def parse_sort(sort_keys_allowed, default_sort=None, default_order=1):
    """
    Lê sort e order da query string.
    sort_keys_allowed: lista de chaves permitidas para ordenação.
    default_sort: chave padrão (ex: "nome").
    default_order: 1 (asc) ou -1 (desc).
    Retorna lista de tuplas para .sort() do MongoDB.
    """
    sort_key = request.args.get("sort", default_sort)
    order_str = request.args.get("order", "asc").lower()
    order = -1 if order_str == "desc" else 1
    if sort_key and (sort_keys_allowed is None or sort_key in sort_keys_allowed):
        return [(sort_key, order)]
    if default_sort:
        return [(default_sort, default_order)]
    return []


def parse_fields(projection_keys_allowed):
    """
    Lê fields=id,nome,codigo da query string e monta projection para find().
    projection_keys_allowed: lista de chaves permitidas (None = todas).
    Retorna dict de projection ou None (sem projection).
    """
    raw = request.args.get("fields")
    if not raw:
        return None
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    if not keys:
        return None
    if projection_keys_allowed is not None:
        keys = [k for k in keys if k in projection_keys_allowed]
    if not keys:
        return None
    proj = {k: 1 for k in keys}
    if "_id" not in proj:
        proj["_id"] = 1  # _id sempre incluído por padrão no MongoDB
    return proj


def apply_list_options(cursor, collection, filtro, sort_list=None, page=1, per_page=50):
    """
    Aplica ordenação, skip e limit ao cursor e obtém total.
    Retorna (lista de docs, total).
    Use projection em collection.find(filtro, projection) antes de passar o cursor.
    """
    total = collection.count_documents(filtro)
    if sort_list:
        cursor = cursor.sort(sort_list)
    cursor = cursor.skip((page - 1) * per_page).limit(per_page)
    docs = list(cursor)
    return docs, total


def rest_list_response(docs, total, page, per_page, serialize=True):
    """Resposta REST padronizada para listas (com meta de paginação)."""
    from db import serialize_doc
    data = serialize_doc(docs) if serialize else docs
    total_pages = (total + per_page - 1) // per_page if per_page else 0
    return jsonify({
        "data": data,
        "meta": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
        }
    })


def rest_item_response(doc, serialize=True):
    """Resposta REST para um único recurso (GET by id)."""
    from db import serialize_doc
    if doc is None:
        return jsonify({"error": "Recurso não encontrado"}), 404
    return jsonify(serialize_doc(doc) if serialize else doc)
