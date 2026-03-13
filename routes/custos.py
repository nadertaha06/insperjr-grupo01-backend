from flask import Blueprint, jsonify, request
from db import db

custos_routes = Blueprint("custos", __name__)


@custos_routes.route("/custos")
def listar_custos():
    filtro = {}

    sku_id = request.args.get("sku_id")
    if sku_id:
        filtro["sku_id"] = sku_id

    tipo = request.args.get("tipo")
    if tipo:
        filtro["tipo"] = tipo

    custos = list(db["custos"].find(filtro))
    return jsonify(custos)



@custos_routes.route("/custos/<sku_id>")
def buscar_custos_por_sku(sku_id):
    custos = list(db["custos"].find({"sku_id": sku_id}))
    return jsonify(custos)
