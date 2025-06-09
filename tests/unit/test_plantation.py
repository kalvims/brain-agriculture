"""Plantation Unit Tests"""


# Teste de Listagem de Plantations
def test_list_plantations(test_client, plantation_data):
    # Cria algumas plantations para testar
    for _ in range(2):
        test_client.post("/api/v1/plantation/", json=plantation_data)

    # Faz a requisição para listar as plantations
    response = test_client.get("/api/v1/plantation/")
    assert response.status_code == 200
    assert len(response.json()) == 2


# Teste de Criação de Plantation
def test_create_plantation(test_client, plantation_data):
    response = test_client.post("/api/v1/plantation/", json=plantation_data)
    assert response.status_code == 200
    assert response.json()["name"] == plantation_data["name"]
    assert response.json()["description"] == plantation_data["description"]


# Teste de Obtenção de Plantation por ID
def test_get_plantation_by_id(test_client, plantation_data):
    # Cria uma plantation para testar
    create_response = test_client.post(
        "/api/v1/plantation/", json=plantation_data)
    plantation_id = create_response.json()["id"]

    # Faz a requisição para obter a plantation por ID
    response = test_client.get(f"/api/v1/plantation/{plantation_id}")
    assert response.status_code == 200
    assert response.json()["id"] == plantation_id
    assert response.json()["name"] == plantation_data["name"]


# Teste de Atualização de Plantation
def test_update_plantation(test_client, plantation_data,
                           updated_plantation_data):
    # Cria uma plantation para testar
    create_response = test_client.post(
        "/api/v1/plantation/", json=plantation_data)
    plantation_id = create_response.json()["id"]

    # Atualiza a plantation
    response = test_client.put(
        f"/api/v1/plantation/{plantation_id}", json=updated_plantation_data
    )
    assert response.status_code == 200
    assert response.json()["name"] == updated_plantation_data["name"]
    assert response.json()[
        "description"] == updated_plantation_data["description"]


# Teste de Deleção de Plantation
def test_delete_plantation(test_client, plantation_data):
    # Cria uma plantation para testar
    create_response = test_client.post(
        "/api/v1/plantation/", json=plantation_data)
    plantation_id = create_response.json()["id"]

    # Faz a requisição para deletar a plantation
    response = test_client.delete(f"/api/v1/plantation/{plantation_id}")
    assert response.status_code == 200
    assert response.json()["id"] == plantation_id

    # Verifica se a plantation foi realmente deletada
    get_response = test_client.get(f"/api/v1/plantation/{plantation_id}")
    assert get_response.status_code == 404
