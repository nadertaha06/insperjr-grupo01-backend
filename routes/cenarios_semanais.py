from flask import Blueprint, request
from db import db
from utils.rest import (
    parse_pagination,
    parse_sort,
    parse_fields,
    apply_list_options,
    rest_list_response,
)

cenarios_routes = Blueprint("cenarios_semanais", __name__)

CENARIOS_SORT_KEYS = ["sku_id", "cenario", "geo_regiao", "sku_nome"]
CENARIOS_PROJECTION_KEYS = ["_id", "sku_id", "sku_nome", "cenario", "geo_regiao", "semanas"]


@cenarios_routes.route("/cenarios-semanais", methods=["GET"])
def listar_cenarios():
    filtro = {}
    if request.args.get("sku_id"):
        filtro["sku_id"] = request.args.get("sku_id")
    if request.args.get("cenario"):
        filtro["cenario"] = request.args.get("cenario")
    if request.args.get("geo_regiao"):
        filtro["geo_regiao"] = request.args.get("geo_regiao")

    page, per_page = parse_pagination()
    sort_list = parse_sort(CENARIOS_SORT_KEYS, default_sort="sku_id")
    projection = parse_fields(CENARIOS_PROJECTION_KEYS)

    cursor = db["cenarios_semanais"].find(filtro, projection)
    docs, total = apply_list_options(
        cursor, db["cenarios_semanais"], filtro, sort_list=sort_list, page=page, per_page=per_page
    )
    return rest_list_response(docs, total, page, per_page)


@cenarios_routes.route("/cenarios-semanais/<sku_id>", methods=["GET"])
def buscar_cenarios_por_sku(sku_id):
    filtro = {"sku_id": sku_id}
    page, per_page = parse_pagination()
    sort_list = parse_sort(CENARIOS_SORT_KEYS, default_sort="cenario")
    projection = parse_fields(CENARIOS_PROJECTION_KEYS)

    cursor = db["cenarios_semanais"].find(filtro, projection)
    docs, total = apply_list_options(
        cursor, db["cenarios_semanais"], filtro, sort_list=sort_list, page=page, per_page=per_page
    )
    return rest_list_response(docs, total, page, per_page)
