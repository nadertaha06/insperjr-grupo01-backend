from flask import Blueprint, jsonify, request
from db import db

cenario_atual_routes = Blueprint("cenario_atual_br", __name__)

@cenario_atual_routes.route("/cenario-atual-br")
def listar_cenario_atual():
    filtro = {}

    sku_id = request.args.get("sku_id")
    if sku_id:
        filtro["sku_id"] = sku_id

    geo_regiao = request.args.get("geo_regiao")
    if geo_regiao:
        filtro["geo_regiao"] = geo_regiao

    is_total = request.args.get("is_total")
    if is_total is not None:
        filtro["is_total"] = is_total.lower() == "true"

    cenarios = list(db["cenario_atual_br"].find(filtro))
    return jsonify(cenarios)


# GET /cenario-atual-br/<geo_regiao> → dados de uma região específica
@cenario_atual_routes.route("/cenario-atual-br/<geo_regiao>")
def buscar_por_regiao(geo_regiao):
    cenarios = list(db["cenario_atual_br"].find({"geo_regiao": geo_regiao}))
    return jsonify(cenarios)
