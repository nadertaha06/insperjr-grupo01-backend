import os
from flask import Flask
from flask_cors import CORS

from routes.skus import skus_routes
from routes.custos import custos_routes
from routes.transferencias import transferencias_routes
from routes.producao_pcp import producao_routes
from routes.cenarios_semanais import cenarios_routes
from routes.cenario_atual_br import cenario_atual_routes

app = Flask(__name__)

# Em produção, troque "*" pela URL do seu frontend
# Ex: FRONTEND_URL=https://meu-frontend.vercel.app
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
CORS(app, origins=FRONTEND_URL)

# Registra todas as rotas
app.register_blueprint(skus_routes)
app.register_blueprint(custos_routes)
app.register_blueprint(transferencias_routes)
app.register_blueprint(producao_routes)
app.register_blueprint(cenarios_routes)
app.register_blueprint(cenario_atual_routes)

if __name__ == "__main__":
    from waitress import serve
    print("Servidor rodando em http://localhost:5000")
    serve(app, host="0.0.0.0", port=5000)
