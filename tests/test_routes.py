"""
Testa cada rota da API contra os JSON em data/.
Requer MongoDB com database ambev populado (python -m scripts.seed_ambev).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
sys.path.insert(0, ROOT)

# Mapeamento: coleção -> arquivo JSON (nome sem extensão para "custos (1).json" -> custos)
COLLECTION_TO_JSON = {
    "skus": "skus.json",
    "cenario_atual_br": "cenario_atual_br.json",
    "cenarios_semanais": "cenarios_semanais.json",
    "custos": "custos (1).json",
    "producao_pcp": "producao_pcp.json",
    "transferencias": "transferencias.json",
}


def load_json(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_skus_list(client):
    expected = load_json("skus.json")
    assert expected is not None, "skus.json não encontrado"
    r = client.get("/api/v1/skus?per_page=100")
    assert r.status_code == 200, f"GET /skus status {r.status_code}"
    body = r.get_json()
    assert "data" in body and "meta" in body, "Resposta sem data/meta"
    assert body["meta"]["total"] == len(expected), f"total esperado {len(expected)}, obtido {body['meta']['total']}"
    ids_resp = {d["_id"] for d in body["data"]}
    ids_exp = {d["_id"] for d in expected}
    assert ids_resp == ids_exp, f"IDs diferentes: esperado {ids_exp}, obtido {ids_resp}"
    # Primeiro item deve bater (campos)
    first_exp = expected[0]
    first_resp = next((d for d in body["data"] if d["_id"] == first_exp["_id"]), None)
    assert first_resp is not None, "Primeiro SKU não encontrado na resposta"
    for k in first_exp:
        assert k in first_resp and first_resp[k] == first_exp[k], f"Campo {k} diferente"
    return True


def test_skus_filter_container_type(client):
    expected = load_json("skus.json")
    longneck = [d for d in expected if d.get("container_type") == "LONG NECK"]
    r = client.get("/api/v1/skus?container_type=LONG%20NECK&per_page=50")
    assert r.status_code == 200
    body = r.get_json()
    assert body["meta"]["total"] == len(longneck)
    assert all(d["container_type"] == "LONG NECK" for d in body["data"])
    return True


def test_skus_by_id(client):
    expected = load_json("skus.json")
    sku_id = expected[0]["_id"]
    r = client.get(f"/api/v1/skus/{sku_id}")
    assert r.status_code == 200, f"GET /skus/{{id}} status {r.status_code}"
    body = r.get_json()
    assert body["_id"] == sku_id
    for k in expected[0]:
        assert body.get(k) == expected[0][k], f"Campo {k} diferente"
    # 404 para id inexistente
    r404 = client.get("/api/v1/skus/id_inexistente_xyz")
    assert r404.status_code == 404
    return True


def test_cenario_atual_br_list(client):
    expected = load_json("cenario_atual_br.json")
    assert expected is not None
    r = client.get("/api/v1/cenario-atual-br?per_page=100")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(expected)
    ids_resp = {d["_id"] for d in body["data"]}
    ids_exp = {d["_id"] for d in expected}
    assert ids_resp == ids_exp
    return True


def test_cenarios_semanais_list(client):
    expected = load_json("cenarios_semanais.json")
    assert expected is not None
    r = client.get("/api/v1/cenarios-semanais?per_page=500")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(expected)
    ids_resp = {d["_id"] for d in body["data"]}
    ids_exp = {d["_id"] for d in expected}
    assert ids_resp == ids_exp
    return True


def test_custos_list(client):
    expected = load_json("custos (1).json")
    assert expected is not None
    r = client.get("/api/v1/custos?per_page=100")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(expected)
    ids_resp = {d["_id"] for d in body["data"]}
    ids_exp = {d["_id"] for d in expected}
    assert ids_resp == ids_exp
    return True


def test_producao_pcp_list(client):
    expected = load_json("producao_pcp.json")
    assert expected is not None
    r = client.get("/api/v1/producao-pcp?per_page=100")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(expected)
    ids_resp = {d["_id"] for d in body["data"]}
    ids_exp = {d["_id"] for d in expected}
    assert ids_resp == ids_exp
    return True


def test_transferencias_list(client):
    expected = load_json("transferencias.json")
    assert expected is not None
    r = client.get("/api/v1/transferencias?per_page=100")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(expected)
    ids_resp = {d["_id"] for d in body["data"]}
    ids_exp = {d["_id"] for d in expected}
    assert ids_resp == ids_exp
    return True


def test_dashboard(client):
    r = client.get("/api/v1/dashboard")
    assert r.status_code == 200
    body = r.get_json()
    assert "meta" in body and "contagens" in body["meta"]
    assert "totais_brasil" in body
    assert "skus" in body
    counts = body["meta"]["contagens"]
    expected_skus = len(load_json("skus.json"))
    assert counts["skus"] == expected_skus, f"contagens.skus esperado {expected_skus}, obtido {counts['skus']}"
    return True


def test_cenario_atual_br_by_region(client):
    expected = load_json("cenario_atual_br.json")
    total_docs = [d for d in expected if d.get("geo_regiao") == "TOTAL"]
    r = client.get("/api/v1/cenario-atual-br/TOTAL?per_page=10")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(total_docs)
    assert all(d["geo_regiao"] == "TOTAL" for d in body["data"])
    return True


def test_custos_by_sku(client):
    expected = load_json("custos (1).json")
    sku_id = "sku_colorado_lager"
    expected_for_sku = [d for d in expected if d["sku_id"] == sku_id]
    r = client.get(f"/api/v1/custos/{sku_id}?per_page=50")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(expected_for_sku)
    assert all(d["sku_id"] == sku_id for d in body["data"])
    return True


def test_cenarios_semanais_by_sku(client):
    expected = load_json("cenarios_semanais.json")
    sku_id = "sku_patagonia_amber"
    expected_for_sku = [d for d in expected if d["sku_id"] == sku_id]
    r = client.get(f"/api/v1/cenarios-semanais/{sku_id}?per_page=50")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(expected_for_sku)
    return True


def test_producao_pcp_by_sku(client):
    expected = load_json("producao_pcp.json")
    sku_id = "sku_goose_midway"
    expected_for_sku = [d for d in expected if d["sku_id"] == sku_id]
    r = client.get(f"/api/v1/producao-pcp/{sku_id}?per_page=50")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(expected_for_sku)
    return True


def test_transferencias_by_sku(client):
    expected = load_json("transferencias.json")
    sku_id = "sku_goose_midway"
    expected_for_sku = [d for d in expected if d["sku_id"] == sku_id]
    r = client.get(f"/api/v1/transferencias/{sku_id}?per_page=50")
    assert r.status_code == 200
    body = r.get_json()
    assert "data" in body and "meta" in body
    assert body["meta"]["total"] == len(expected_for_sku)
    return True


def run_all():
    from app import app
    client = app.test_client()
    results = []
    tests = [
        ("GET /api/v1/skus (lista)", test_skus_list),
        ("GET /api/v1/skus?container_type= (filtro)", test_skus_filter_container_type),
        ("GET /api/v1/skus/<id>", test_skus_by_id),
        ("GET /api/v1/cenario-atual-br", test_cenario_atual_br_list),
        ("GET /api/v1/cenario-atual-br/<regiao>", test_cenario_atual_br_by_region),
        ("GET /api/v1/cenarios-semanais", test_cenarios_semanais_list),
        ("GET /api/v1/cenarios-semanais/<sku_id>", test_cenarios_semanais_by_sku),
        ("GET /api/v1/custos", test_custos_list),
        ("GET /api/v1/custos/<sku_id>", test_custos_by_sku),
        ("GET /api/v1/producao-pcp", test_producao_pcp_list),
        ("GET /api/v1/producao-pcp/<sku_id>", test_producao_pcp_by_sku),
        ("GET /api/v1/transferencias", test_transferencias_list),
        ("GET /api/v1/transferencias/<sku_id>", test_transferencias_by_sku),
        ("GET /api/v1/dashboard", test_dashboard),
    ]
    for name, fn in tests:
        try:
            fn(client)
            results.append((name, "OK"))
        except AssertionError as e:
            results.append((name, f"FALHA: {e}"))
        except Exception as e:
            results.append((name, f"ERRO: {e}"))
    return results


if __name__ == "__main__":
    results = run_all()
    for name, status in results:
        print(f"  {name}: {status}")
    failures = [r for r in results if r[1] != "OK"]
    sys.exit(1 if failures else 0)
