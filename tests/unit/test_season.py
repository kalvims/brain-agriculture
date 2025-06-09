"""Seasons Unit Tests"""

def test_create_season(test_client, season_data):
    """
    Testa a criação de uma nova safra.
    """
    response = test_client.post("/api/v1/season/", json=season_data)
    assert response.status_code == 200
    assert response.json()["year"] == 2023
    assert response.json()["description"] == "Safra de Verão 2023"

def test_get_season(test_client, season_data):
    """
    Testa a obtenção de uma safra pelo ID.
    """
    # Cria uma safra para buscar
    create_response = test_client.post("/api/v1/season/", json=season_data)
    season_id = create_response.json()["id"]

    # Busca a safra criada
    get_response = test_client.get(f"/api/v1/season/{season_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == season_id
    assert get_response.json()["year"] == 2023

def test_list_seasons(test_client, season_data):
    """
    Testa a listagem de todas as safras.
    """
    # Cria uma safra para listar
    test_client.post("/api/v1/season/", json=season_data)

    # Lista as safras
    list_response = test_client.get("/api/v1/season/")
    assert list_response.status_code == 200
    assert len(list_response.json()) > 0

def test_update_season(test_client, season_data, updated_season_data):
    """
    Testa a atualização de uma safra existente.
    """
    # Cria uma safra para atualizar
    create_response = test_client.post("/api/v1/season/", json=season_data)
    season_id = create_response.json()["id"]

    # Atualiza a safra
    update_response = test_client.put(
        f"/api/v1/season/{season_id}", json=updated_season_data
    )
    assert update_response.status_code == 200
    assert update_response.json()["year"] == 2024
    assert update_response.json()["description"] == "Safra de Verão 2024"

def test_delete_season(test_client, season_data):
    """
    Testa a remoção de uma safra existente.
    """
    # Cria uma safra para deletar
    create_response = test_client.post("/api/v1/season/", json=season_data)
    season_id = create_response.json()["id"]

    # Deleta a safra
    delete_response = test_client.delete(f"/api/v1/season/{season_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == season_id

    # Verifica se a safra foi realmente deletada
    get_response = test_client.get(f"/api/v1/season/{season_id}")
    assert get_response.status_code == 404
