import os
from flask import Flask, jsonify
from flask_cors import CORS

from routes.skus import skus_routes
from routes.custos import custos_routes
from routes.transferencias import transferencias_routes
from routes.producao_pcp import producao_routes
from routes.cenarios_semanais import cenarios_routes
from routes.cenario_atual_br import cenario_atual_routes
from routes.dashboard import dashboard_routes

app = Flask(__name__)

# Em produção, troque "*" pela URL do seu frontend
# Ex: FRONTEND_URL=https://meu-frontend.vercel.app
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
CORS(app, origins=FRONTEND_URL)

# Prefixo RESTful versionado para o dashboard executivo
API_PREFIX = "/api/v1"
app.register_blueprint(skus_routes, url_prefix=API_PREFIX)
app.register_blueprint(custos_routes, url_prefix=API_PREFIX)
app.register_blueprint(transferencias_routes, url_prefix=API_PREFIX)
app.register_blueprint(producao_routes, url_prefix=API_PREFIX)
app.register_blueprint(cenarios_routes, url_prefix=API_PREFIX)
app.register_blueprint(cenario_atual_routes, url_prefix=API_PREFIX)
app.register_blueprint(dashboard_routes, url_prefix=API_PREFIX)


@app.route("/")
def index():
    """Raiz: informações da API e links úteis."""
    return jsonify({
        "api": "Ambev Dashboard Executivo",
        "version": "1.0",
        "docs": "Endpoints REST em /api/v1",
        "recursos": [
            f"{API_PREFIX}/skus",
            f"{API_PREFIX}/custos",
            f"{API_PREFIX}/transferencias",
            f"{API_PREFIX}/producao-pcp",
            f"{API_PREFIX}/cenarios-semanais",
            f"{API_PREFIX}/cenario-atual-br",
            f"{API_PREFIX}/dashboard",
        ],
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
