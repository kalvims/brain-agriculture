"""Integration Tests for Productor Flow"""

def test_productor_flow(test_client, user_payload, farm_payload):
    # Cria um produtor
    productor_response = test_client.post(
        "/api/v1/productor/", json=user_payload)
    productor_id = productor_response.json()["id"]
    farm_payload["productor_id"] = productor_id

    # Cria uma fazenda
    farm_response = test_client.post("/api/v1/farm/", json=farm_payload)
    farm_id = farm_response.json()["id"]

    # Busca as estatísticas de fazendas
    total_farms_response = test_client.get("/api/v1/reports/total-farms")
    assert total_farms_response.status_code == 200
    assert total_farms_response.json()["total_farms"] == 1

    # Busca as estatísticas de uso do solo
    ground_use_stats_response = test_client.get(
        "/api/v1/reports/ground-use-statistics")
    assert ground_use_stats_response.status_code == 200
    ground_use_stats = ground_use_stats_response.json()
    assert ground_use_stats["total_area"] == 100.0 