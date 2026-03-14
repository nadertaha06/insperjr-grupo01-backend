from flask import Blueprint, request
from db import db
from utils.rest import (
    parse_pagination,
    parse_sort,
    parse_fields,
    apply_list_options,
    rest_list_response,
)

producao_routes = Blueprint("producao_pcp", __name__)

PCP_SORT_KEYS = ["sku_id", "localidade", "linha", "container_type"]
PCP_PROJECTION_KEYS = ["_id", "sku_id", "sku_nome", "localidade", "linha", "container_type", "capacidade", "semanas"]


@producao_routes.route("/producao-pcp", methods=["GET"])
def listar_producao():
    filtro = {}
    if request.args.get("sku_id"):
        filtro["sku_id"] = request.args.get("sku_id")
    if request.args.get("localidade"):
        filtro["localidade"] = {"$regex": request.args.get("localidade"), "$options": "i"}
    if request.args.get("linha"):
        filtro["linha"] = request.args.get("linha")

    page, per_page = parse_pagination()
    sort_list = parse_sort(PCP_SORT_KEYS, default_sort="localidade")
    projection = parse_fields(PCP_PROJECTION_KEYS)

    cursor = db["producao_pcp"].find(filtro, projection)
    docs, total = apply_list_options(
        cursor, db["producao_pcp"], filtro, sort_list=sort_list, page=page, per_page=per_page
    )
    return rest_list_response(docs, total, page, per_page)


@producao_routes.route("/producao-pcp/<sku_id>", methods=["GET"])
def buscar_producao_por_sku(sku_id):
    filtro = {"sku_id": sku_id}
    page, per_page = parse_pagination()
    sort_list = parse_sort(PCP_SORT_KEYS, default_sort="localidade")
    projection = parse_fields(PCP_PROJECTION_KEYS)

    cursor = db["producao_pcp"].find(filtro, projection)
    docs, total = apply_list_options(
        cursor, db["producao_pcp"], filtro, sort_list=sort_list, page=page, per_page=per_page
    )
    return rest_list_response(docs, total, page, per_page)
