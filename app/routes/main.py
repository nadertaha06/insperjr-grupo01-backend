from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return jsonify({"message": "API running"})


@main_bp.get("/health")
def health():
    return jsonify({"status": "ok"})
