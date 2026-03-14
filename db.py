from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

# Conecta ao MongoDB. Database "ambev" para o dashboard executivo.
# Coleções: skus, cenario_atual_br, cenarios_semanais, custos, producao_pcp, transferencias
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ambev")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def serialize_doc(doc):
    """Converte documento MongoDB para JSON-serializável (_id como string)."""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    if isinstance(doc, dict):
        out = {}
        for k, v in doc.items():
            if k == "_id" and isinstance(v, ObjectId):
                out[k] = str(v)
            else:
                out[k] = serialize_doc(v)
        return out
    return doc
