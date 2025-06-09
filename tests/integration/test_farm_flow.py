"""Integration Tests for Farm Flow"""

def test_farm_flow(test_client, user_payload, farm_payload, plantation_data, season_data, farm_plantation_season_data):
    # Cria um produtor
    productor_response = test_client.post(
        "/api/v1/productor/", json=user_payload)
    productor_id = productor_response.json()["id"]
    farm_payload["productor_id"] = productor_id

    # Cria uma fazenda
    farm_response = test_client.post("/api/v1/farm/", json=farm_payload)
    farm_id = farm_response.json()["id"]

    # Cria uma plantation
    plantation_response = test_client.post(
        "/api/v1/plantation/", json=plantation_data)
    plantation_id = plantation_response.json()["id"]

    # Cria uma season
    season_response = test_client.post("/api/v1/season/", json=season_data)
    season_id = season_response.json()["id"]

    # Adiciona a plantation à season na farm
    farm_plantation_season_data["plantation_id"] = plantation_id
    farm_plantation_season_data["season_id"] = season_id
    add_plantation_response = test_client.put(
        f"/api/v1/farm/{farm_id}/add-plantation", json=farm_plantation_season_data
    )
    assert add_plantation_response.status_code == 200

    # Busca as estatísticas de plantações
    plantation_stats_response = test_client.get(
        "/api/v1/reports/plantation-statistics")
    assert plantation_stats_response.status_code == 200
    plantation_stats = plantation_stats_response.json()
    assert len(plantation_stats) > 0

    # Busca as estatísticas de uso do solo
    ground_use_stats_response = test_client.get(
        "/api/v1/reports/ground-use-statistics")
    assert ground_use_stats_response.status_code == 200
    ground_use_stats = ground_use_stats_response.json()
    assert ground_use_stats["total_area"] == 100.0 