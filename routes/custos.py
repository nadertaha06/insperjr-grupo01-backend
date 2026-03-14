from flask import Blueprint, request
from db import db
from utils.rest import (
    parse_pagination,
    parse_sort,
    parse_fields,
    apply_list_options,
    rest_list_response,
)

custos_routes = Blueprint("custos", __name__)

CUSTOS_SORT_KEYS = ["sku_id", "tipo", "origem", "destino", "reais_por_hl"]
CUSTOS_PROJECTION_KEYS = ["_id", "sku_id", "sku_nome", "tipo", "origem", "destino", "reais_por_hl"]


@custos_routes.route("/custos", methods=["GET"])
def listar_custos():
    filtro = {}
    if request.args.get("sku_id"):
        filtro["sku_id"] = request.args.get("sku_id")
    if request.args.get("tipo"):
        filtro["tipo"] = request.args.get("tipo")
    if request.args.get("origem"):
        filtro["origem"] = {"$regex": request.args.get("origem"), "$options": "i"}
    if request.args.get("destino"):
        filtro["destino"] = {"$regex": request.args.get("destino"), "$options": "i"}

    page, per_page = parse_pagination()
    sort_list = parse_sort(CUSTOS_SORT_KEYS, default_sort="sku_id")
    projection = parse_fields(CUSTOS_PROJECTION_KEYS)

    cursor = db["custos"].find(filtro, projection)
    docs, total = apply_list_options(cursor, db["custos"], filtro, sort_list=sort_list, page=page, per_page=per_page)
    return rest_list_response(docs, total, page, per_page)


@custos_routes.route("/custos/<sku_id>", methods=["GET"])
def buscar_custos_por_sku(sku_id):
    """Lista custos de um SKU (com paginação)."""
    filtro = {"sku_id": sku_id}
    page, per_page = parse_pagination()
    sort_list = parse_sort(CUSTOS_SORT_KEYS, default_sort="tipo")
    projection = parse_fields(CUSTOS_PROJECTION_KEYS)

    cursor = db["custos"].find(filtro, projection)
    docs, total = apply_list_options(cursor, db["custos"], filtro, sort_list=sort_list, page=page, per_page=per_page)
    return rest_list_response(docs, total, page, per_page)
