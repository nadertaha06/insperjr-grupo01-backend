from flask import Blueprint, jsonify, request
from db import db

producao_routes = Blueprint("producao_pcp", __name__)


@producao_routes.route("/producao-pcp")
def listar_producao():
    filtro = {}

    sku_id = request.args.get("sku_id")
    if sku_id:
        filtro["sku_id"] = sku_id

    localidade = request.args.get("localidade")
    if localidade:
        filtro["localidade"] = {"$regex": localidade, "$options": "i"}

    producao = list(db["producao_pcp"].find(filtro))
    return jsonify(producao)



@producao_routes.route("/producao-pcp/<sku_id>")
def buscar_producao_por_sku(sku_id):
    producao = list(db["producao_pcp"].find({"sku_id": sku_id}))
    return jsonify(producao)
