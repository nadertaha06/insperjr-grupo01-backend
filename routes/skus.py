from flask import Blueprint, jsonify, request
from db import db

skus_routes = Blueprint("skus", __name__)


@skus_routes.route("/skus")
def listar_skus():
    filtro = {}

    container_type = request.args.get("container_type")
    if container_type:
        filtro["container_type"] = container_type

    skus = list(db["skus"].find(filtro, {"_id": 1, "codigo": 1, "nome": 1, "container_type": 1}))
    return jsonify(skus)


@skus_routes.route("/skus/<sku_id>")
def buscar_sku(sku_id):
    sku = db["skus"].find_one({"_id": sku_id})
    if not sku:
        return jsonify({"erro": "SKU não encontrado"}), 404
    return jsonify(sku)
