import requests

API_URL = 'http://localhost:8000'

def fetch_optimal_station(x: float, y: float, method: str, dataset: str):
    return requests.get('%s?x=%s&y=%s&method=%s&dataset=%s' % (API_URL, x, y, method, dataset))

def test_simple():
    response = fetch_optimal_station(
        x='0.0',
        y='1.0',
        method='simple',
        dataset='5.txt'
    )
    assert response.status_code == 200
    assert response.text == "Best network station for point x=0.0, y=1.0 is x=0.0, y=0.0 with speed 64.0"
    response = fetch_optimal_station(
        x='-100.0',
        y='-100.0',
        method='simple',
        dataset='5.txt'
    )
    assert response.status_code == 200
    assert response.text == "No network station within reach for point x=-100.0, y=-100.0"

def test_numpy():
    response = fetch_optimal_station(
        x='0.0',
        y='1.0',
        method='numpy',
        dataset='5.txt'
    )
    assert response.status_code == 200
    assert response.text == "Best network station for point x=0.0, y=1.0 is x=0.0, y=0.0 with speed 64.0"
    response = fetch_optimal_station(
        x='-100.0',
        y='-100.0',
        method='numpy',
        dataset='5.txt'
    )
    assert response.status_code == 200
    assert response.text == "No network station within reach for point x=-100.0, y=-100.0"

def test_validation():
    response = fetch_optimal_station(
        x='0.0',
        y='0.0',
        method='invalid data',
        dataset='invalid data'
    )
    assert response.status_code == 400
    response = fetch_optimal_station(
        x='invalid_data',
        y='invalid_data',
        method='simple',
        dataset='5.txt'
    )
    assert response.status_code == 400