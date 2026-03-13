from flask import Blueprint, jsonify, request
from db import db

cenarios_routes = Blueprint("cenarios_semanais", __name__)


@cenarios_routes.route("/cenarios-semanais")
def listar_cenarios():
    filtro = {}

    sku_id = request.args.get("sku_id")
    if sku_id:
        filtro["sku_id"] = sku_id

    cenario = request.args.get("cenario")
    if cenario:
        filtro["cenario"] = cenario

    geo_regiao = request.args.get("geo_regiao")
    if geo_regiao:
        filtro["geo_regiao"] = geo_regiao

    cenarios = list(db["cenarios_semanais"].find(filtro))
    return jsonify(cenarios)


# GET /cenarios-semanais/<sku_id> → cenários de um SKU específico
@cenarios_routes.route("/cenarios-semanais/<sku_id>")
def buscar_cenarios_por_sku(sku_id):
    cenarios = list(db["cenarios_semanais"].find({"sku_id": sku_id}))
    return jsonify(cenarios)
