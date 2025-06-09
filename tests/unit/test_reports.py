"""Reports Unit Tests"""

def test_get_total_farms(test_client, user_payload, farm_payload):
    # Cria um produtor
    productor_response = test_client.post(
        "/api/v1/productor/", json=user_payload)
    productor_id = productor_response.json()["id"]
    farm_payload["productor_id"] = productor_id

    # Cria uma fazenda
    test_client.post("/api/v1/farm/", json=farm_payload)

    # Busca o total de fazendas
    response = test_client.get("/api/v1/reports/total-farms")
    assert response.status_code == 200
    assert response.json()["total_farms"] == 1

def test_get_total_area(test_client, user_payload, farm_payload):
    # Cria um produtor
    productor_response = test_client.post(
        "/api/v1/productor/", json=user_payload)
    productor_id = productor_response.json()["id"]
    farm_payload["productor_id"] = productor_id

    # Cria uma fazenda
    test_client.post("/api/v1/farm/", json=farm_payload)

    # Busca a área total das fazendas
    response = test_client.get("/api/v1/reports/total-area")
    assert response.status_code == 200
    assert response.json()["total_area"] == 100.0

def test_get_state_statistics(test_client, user_payload, farm_payload):
    # Cria um produtor
    productor_response = test_client.post(
        "/api/v1/productor/", json=user_payload)
    productor_id = productor_response.json()["id"]
    farm_payload["productor_id"] = productor_id

    # Cria uma fazenda
    test_client.post("/api/v1/farm/", json=farm_payload)

    # Busca as estatísticas por estado
    response = test_client.get("/api/v1/reports/state-statistics")
    assert response.status_code == 200
    state_statistics = response.json()

    # Valida a estrutura e os valores retornados
    assert len(state_statistics) > 0
    for state in state_statistics:
        assert "state" in state
        assert "farms_total" in state
        assert "farms_percent" in state
        assert "plantation_statistics" in state
        assert "ground_use_statistics" in state

        # Valida os valores específicos
        assert state["state"] == "SP"  # O estado da fazenda criada é SP
        assert state["farms_total"] == 1  # Apenas uma fazenda foi criada
        assert state["farms_percent"] == 100.0  # 100% das fazendas estão em SP

        # Valida as estatísticas de plantação
        plantation_stats = state["plantation_statistics"]
        assert "state_total" in plantation_stats
        assert "percent" in plantation_stats
        assert plantation_stats["state_total"] == 0  # Nenhuma plantação foi adicionada
        assert plantation_stats["percent"] == 0.0  # 0% de plantações

        # Valida as estatísticas de uso do solo
        ground_use_stats = state["ground_use_statistics"]
        assert "total_area" in ground_use_stats
        assert "vegetation_area_total" in ground_use_stats
        assert "vegetation_area_percent" in ground_use_stats
        assert "arable_area_total" in ground_use_stats
        assert "arable_area_percent" in ground_use_stats

        assert ground_use_stats["total_area"] == 100.0  # Área total da fazenda
        assert ground_use_stats["vegetation_area_total"] == 30.0  # Área de vegetação
        assert ground_use_stats["vegetation_area_percent"] == 30.0  # 30% de vegetação
        assert ground_use_stats["arable_area_total"] == 50.0  # Área cultivável
        assert ground_use_stats["arable_area_percent"] == 50.0  # 50% de área cultivável

def test_get_plantation_statistics(test_client, user_payload, farm_payload, plantation_data, season_data, farm_plantation_season_data):
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
    test_client.put(
        f"/api/v1/farm/{farm_id}/add-plantation", json=farm_plantation_season_data
    )

    # Busca as estatísticas de plantações
    response = test_client.get("/api/v1/reports/plantation-statistics")
    assert response.status_code == 200
    plantation_statistics = response.json()

    # Valida a estrutura e os valores retornados
    assert len(plantation_statistics) > 0
    for season in plantation_statistics:
        assert "season_id" in season
        assert "season_plantations_total" in season
        assert "statistics" in season

        # Valida os valores específicos
        assert season["season_id"] == season_id  # ID da season criada
        assert season["season_plantations_total"] == 1  # Apenas uma plantation foi adicionada

        # Valida as estatísticas de plantações por season
        for plantation_stat in season["statistics"]:
            assert "plantation_id" in plantation_stat
            assert "total_plantations" in plantation_stat
            assert "percent" in plantation_stat

            assert plantation_stat["plantation_id"] == plantation_id  # ID da plantation criada
            assert plantation_stat["total_plantations"] == 1  # Apenas uma plantation foi adicionada
            assert plantation_stat["percent"] == 100.0  # 100% das plantações são dessa plantation

def test_get_ground_use_statistics(test_client, user_payload, farm_payload):
    # Cria um produtor
    productor_response = test_client.post(
        "/api/v1/productor/", json=user_payload)
    productor_id = productor_response.json()["id"]
    farm_payload["productor_id"] = productor_id

    # Cria uma fazenda
    test_client.post("/api/v1/farm/", json=farm_payload)

    # Busca as estatísticas de uso do solo
    response = test_client.get("/api/v1/reports/ground-use-statistics")
    assert response.status_code == 200
    assert response.json()["total_area"] == 100.0
    assert response.json()["vegetation_area_total"] == 30.0
    assert response.json()["arable_area_total"] == 50.0
