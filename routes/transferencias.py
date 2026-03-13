from flask import Blueprint, jsonify, request
from db import db

transferencias_routes = Blueprint("transferencias", __name__)


@transferencias_routes.route("/transferencias")
def listar_transferencias():
    filtro = {}

    sku_id = request.args.get("sku_id")
    if sku_id:
        filtro["sku_id"] = sku_id

    modal = request.args.get("modal")
    if modal:
        filtro["modal"] = modal

    transferencias = list(db["transferencias"].find(filtro))
    return jsonify(transferencias)



@transferencias_routes.route("/transferencias/<sku_id>")
def buscar_transferencias_por_sku(sku_id):
    transferencias = list(db["transferencias"].find({"sku_id": sku_id}))
    return jsonify(transferencias)
