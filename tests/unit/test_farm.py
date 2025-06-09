"""Farms Unit Tests"""


def test_create_farm(test_client, user_payload, farm_payload):
    productor_response = test_client.post(
        "/api/v1/productor/", json=user_payload)
    productor_id = productor_response.json()["id"]
    farm_payload["productor_id"] = productor_id

    response = test_client.post("/api/v1/farm/", json=farm_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Fazenda Tiao"
    assert response.json()["total_area"] == 100.0


def test_create_farm_invalid_area(
        test_client, user_payload, farm_payload_invalid_area):
    productor_response = test_client.post(
        "/api/v1/productor/", json=user_payload)
    productor_id = productor_response.json()["id"]
    farm_payload_invalid_area["productor_id"] = productor_id

    response = test_client.post(
        "/api/v1/farm/",
        json=farm_payload_invalid_area)
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "The total area is less than the combined area of vegetation and arable land"
    )


def test_create_farm_invalid_productor(test_client, farm_payload):
    # Usa um productor_id inválido
    farm_payload["productor_id"] = 888
    response = test_client.post("/api/v1/farm/", json=farm_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Productor not found"


def test_add_plantation_to_farm(
    test_client, user_payload, farm_payload,
    plantation_data, season_data, farm_plantation_season_data
):
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
    assert add_plantation_response.json()["plantation_id"] == plantation_id
    assert add_plantation_response.json()["season_id"] == season_id


def test_get_farm_plantations(test_client, user_payload, farm_payload, plantation_data, season_data, farm_plantation_season_data):
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

    # Busca as plantations da farm
    get_plantations_response = test_client.get(
        f"/api/v1/farm/{farm_id}/plantations")
    assert get_plantations_response.status_code == 200
    assert len(get_plantations_response.json()) > 0


def test_get_farm_seasons(test_client, user_payload, farm_payload, plantation_data, season_data, farm_plantation_season_data):
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

    # Busca as seasons da farm
    get_seasons_response = test_client.get(f"/api/v1/farm/{farm_id}/seasons")
    assert get_seasons_response.status_code == 200
    assert len(get_seasons_response.json()) > 0
