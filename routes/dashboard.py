"""
Endpoint agregado para o dashboard executivo.
Uma única chamada retorna resumos e totais para alimentar KPIs e gráficos.
"""
from flask import Blueprint, jsonify, request
from db import db, serialize_doc

dashboard_routes = Blueprint("dashboard", __name__)


@dashboard_routes.route("/dashboard", methods=["GET"])
def resumo_dashboard():
    """
    GET /api/v1/dashboard
    Retorna resumo para o frontend: totais por coleção, cenário Brasil (totais)
    e opcionalmente amostra de SKUs. Reduz número de requisições do front.
    """
    # Contagens por coleção (útil para cards e indicadores)
    contagens = {
        "skus": db["skus"].count_documents({}),
        "cenario_atual_br": db["cenario_atual_br"].count_documents({}),
        "cenarios_semanais": db["cenarios_semanais"].count_documents({}),
        "custos": db["custos"].count_documents({}),
        "producao_pcp": db["producao_pcp"].count_documents({}),
        "transferencias": db["transferencias"].count_documents({}),
    }

    # Cenário atual Brasil: apenas totais (is_total=True) para visão executiva
    totais_br = list(
        db["cenario_atual_br"].find({"is_total": True}).limit(20)
    )
    totais_br = serialize_doc(totais_br)

    # Lista enxuta de SKUs para dropdowns/selects (id + nome)
    incluir_skus = request.args.get("incluir_skus", "true").lower() == "true"
    skus_resumo = []
    if incluir_skus:
        skus_resumo = list(
            db["skus"].find({}, {"_id": 1, "nome": 1, "codigo": 1}).sort("nome", 1)
        )
        skus_resumo = serialize_doc(skus_resumo)

    # Regiões disponíveis no cenário atual (para filtros)
    regioes = db["cenario_atual_br"].distinct("geo_regiao")

    return jsonify({
        "meta": {
            "contagens": contagens,
            "regioes": regioes,
        },
        "totais_brasil": totais_br,
        "skus": skus_resumo,
    })
