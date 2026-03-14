from flask import Blueprint, request
from db import db
from utils.rest import (
    parse_pagination,
    parse_sort,
    parse_fields,
    apply_list_options,
    rest_list_response,
)

cenario_atual_routes = Blueprint("cenario_atual_br", __name__)

CENARIO_ATUAL_SORT_KEYS = ["sku_id", "geo_regiao", "geo_nome", "is_total"]
CENARIO_ATUAL_PROJECTION_KEYS = ["_id", "sku_id", "geo_regiao", "geo_nome", "is_total", "meses"]


@cenario_atual_routes.route("/cenario-atual-br", methods=["GET"])
def listar_cenario_atual():
    filtro = {}
    if request.args.get("sku_id"):
        filtro["sku_id"] = request.args.get("sku_id")
    if request.args.get("geo_regiao"):
        filtro["geo_regiao"] = request.args.get("geo_regiao")
    if request.args.get("is_total") is not None:
        filtro["is_total"] = request.args.get("is_total").lower() == "true"

    page, per_page = parse_pagination()
    sort_list = parse_sort(CENARIO_ATUAL_SORT_KEYS, default_sort="geo_regiao")
    projection = parse_fields(CENARIO_ATUAL_PROJECTION_KEYS)

    cursor = db["cenario_atual_br"].find(filtro, projection)
    docs, total = apply_list_options(
        cursor, db["cenario_atual_br"], filtro, sort_list=sort_list, page=page, per_page=per_page
    )
    return rest_list_response(docs, total, page, per_page)


@cenario_atual_routes.route("/cenario-atual-br/<geo_regiao>", methods=["GET"])
def buscar_por_regiao(geo_regiao):
    """Região por código (ex: SP, MG, TOTAL)."""
    filtro = {"geo_regiao": geo_regiao}
    page, per_page = parse_pagination()
    sort_list = parse_sort(CENARIO_ATUAL_SORT_KEYS, default_sort="sku_id")
    projection = parse_fields(CENARIO_ATUAL_PROJECTION_KEYS)

    cursor = db["cenario_atual_br"].find(filtro, projection)
    docs, total = apply_list_options(
        cursor, db["cenario_atual_br"], filtro, sort_list=sort_list, page=page, per_page=per_page
    )
    return rest_list_response(docs, total, page, per_page)
