import requests


# тестирование создания кошелька и операции
def test_create_wallet():
    wallet_uuid = "333"
    response = requests.post(url=F"http://localhost:8000/api/v1/wallets/{wallet_uuid}/create")
    assert response.status_code == 200


def test_get_wallet_balance():
    wallet_uuid = "333"
    response = requests.get(url=F"http://localhost:8000/api/v1/wallets/{wallet_uuid}")
    assert response.status_code == 200
    assert response.json()['balance'] == 1000


def test_invalid_get_wallet_balance():
    wallet_uuid = "444"
    response = requests.get(url=F"http://localhost:8000/api/v1/wallets/{wallet_uuid}")
    assert response.status_code == 404


def test_operation():
    wallet_uuid = "333"
    response = requests.post(url=F"http://localhost:8000/api/v1/wallets/{wallet_uuid}/operation",
                             params={"operation_type": "DEPOSIT", "amount": 1000})
    assert response.status_code == 200


def test_invalid_operation():
    wallet_uuid = "333"
    response = requests.post(url=F"http://localhost:8000/api/v1/wallets/{wallet_uuid}/operation",
                             params={"operation_type": "INVALID", "amount": 1000})
    assert response.status_code == 400


def test_insufficiency_funds():
    wallet_uuid = "333"
    response = requests.post(url=F"http://localhost:8000/api/v1/wallets/{wallet_uuid}/operation",
                             params={"operation_type": "WITHDRAW", "amount": 10000})
    assert response.status_code == 400
