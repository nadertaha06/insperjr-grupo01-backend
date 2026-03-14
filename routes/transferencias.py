from flask import Blueprint, request
from db import db
from utils.rest import (
    parse_pagination,
    parse_sort,
    parse_fields,
    apply_list_options,
    rest_list_response,
)

transferencias_routes = Blueprint("transferencias", __name__)

TRANSF_SORT_KEYS = ["sku_id", "modal", "origem", "destino"]
TRANSF_PROJECTION_KEYS = ["_id", "sku_id", "sku_nome", "cod_produto", "origem", "destino", "modal", "semanas"]


@transferencias_routes.route("/transferencias", methods=["GET"])
def listar_transferencias():
    filtro = {}
    if request.args.get("sku_id"):
        filtro["sku_id"] = request.args.get("sku_id")
    if request.args.get("modal"):
        filtro["modal"] = request.args.get("modal")
    if request.args.get("destino_geo"):
        filtro["destino.geo"] = request.args.get("destino_geo")

    page, per_page = parse_pagination()
    sort_list = parse_sort(TRANSF_SORT_KEYS, default_sort="sku_id")
    projection = parse_fields(TRANSF_PROJECTION_KEYS)

    cursor = db["transferencias"].find(filtro, projection)
    docs, total = apply_list_options(
        cursor, db["transferencias"], filtro, sort_list=sort_list, page=page, per_page=per_page
    )
    return rest_list_response(docs, total, page, per_page)


@transferencias_routes.route("/transferencias/<sku_id>", methods=["GET"])
def buscar_transferencias_por_sku(sku_id):
    filtro = {"sku_id": sku_id}
    page, per_page = parse_pagination()
    sort_list = parse_sort(TRANSF_SORT_KEYS, default_sort="modal")
    projection = parse_fields(TRANSF_PROJECTION_KEYS)

    cursor = db["transferencias"].find(filtro, projection)
    docs, total = apply_list_options(
        cursor, db["transferencias"], filtro, sort_list=sort_list, page=page, per_page=per_page
    )
    return rest_list_response(docs, total, page, per_page)
