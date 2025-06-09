"""
Productor Unit Tests
"""


def test_create_productor(test_client, user_payload):
    response = test_client.post("/api/v1/productor/", json=user_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "John McDonald"
    assert response.json()["cpf_cnpj"] == "123.456.789-09"


def test_create_productor_invalid_cpf_cnpj(
        test_client, user_payload_invalid_cpf):

    response = test_client.post(
        "/api/v1/productor/",
        json=user_payload_invalid_cpf)
    assert response.status_code == 400


def test_list_productors(test_client, user_payload):
    response = test_client.post("/api/v1/productor/", json=user_payload)
    # Requisição GET
    response = test_client.get("/api/v1/productor/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "John McDonald"


def test_get_productor_by_id(test_client, user_payload):
    create_response = test_client.post("/api/v1/productor/", json=user_payload)
    productor_id = create_response.json()["id"]

    # Requisição GET
    response = test_client.get(f"/api/v1/productor/{productor_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "John McDonald"


def test_get_user_not_found(test_client):
    response = test_client.get(f"/api/v1/productor/888")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"Productor not found"


def test_update_productor(test_client, user_payload, user_payload_updated):
    create_response = test_client.post("/api/v1/productor/", json=user_payload)
    productor_id = create_response.json()["id"]
    # update
    response = test_client.put(
        f"/api/v1/productor/{productor_id}", json=user_payload_updated
    )
    assert response.status_code == 200
    assert response.json()["name"] == "John McDonald da Silva"


def test_update_productor_invalid_cpf_cnpj(
    test_client, user_payload, user_payload_updated_invalid_cpf
):
    create_response = test_client.post("/api/v1/productor/", json=user_payload)
    productor_id = create_response.json()["id"]

    # update invalid CPF
    response = test_client.put(
        f"/api/v1/productor/{productor_id}", json=user_payload_updated_invalid_cpf
    )
    assert response.status_code == 400


def test_delete_productor(test_client, user_payload):
    create_response = test_client.post("/api/v1/productor/", json=user_payload)
    productor_id = create_response.json()["id"]

    # DELETE
    response = test_client.delete(f"/api/v1/productor/{productor_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "John McDonald"

    # Check Deleted
    get_response = test_client.get(f"/api/v1/productor/{productor_id}")
    assert get_response.status_code == 404
