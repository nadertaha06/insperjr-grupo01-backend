from flask import Blueprint, request
from db import db, serialize_doc
from utils.rest import (
    parse_pagination,
    parse_sort,
    parse_fields,
    apply_list_options,
    rest_list_response,
    rest_item_response,
)

skus_routes = Blueprint("skus", __name__)

# Campos permitidos para ordenação e projeção (dashboard pode pedir só o necessário)
SKUS_SORT_KEYS = ["codigo", "nome", "container_type", "unidade_volume"]
SKUS_PROJECTION_KEYS = ["_id", "codigo", "nome", "container_type", "unidade_volume"]


@skus_routes.route("/skus", methods=["GET"])
def listar_skus():
    filtro = {}
    if request.args.get("container_type"):
        filtro["container_type"] = request.args.get("container_type")
    if request.args.get("codigo"):
        filtro["codigo"] = request.args.get("codigo")

    page, per_page = parse_pagination()
    sort_list = parse_sort(SKUS_SORT_KEYS, default_sort="nome")
    projection = parse_fields(SKUS_PROJECTION_KEYS)

    cursor = db["skus"].find(filtro, projection)
    docs, total = apply_list_options(cursor, db["skus"], filtro, sort_list=sort_list, page=page, per_page=per_page)
    return rest_list_response(docs, total, page, per_page)


@skus_routes.route("/skus/<sku_id>", methods=["GET"])
def buscar_sku(sku_id):
    sku = db["skus"].find_one({"_id": sku_id})
    return rest_item_response(sku)
