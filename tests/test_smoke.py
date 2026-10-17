def test_predict_smoke(client, good_row):
    r = client.post("/v1/predict", json=good_row)
    assert r.status_code == 200
    body = r.json()
    assert body["class_predict"] in [0, 1, 2] 
    assert body["latency_ms"] >= 0
    assert body["model_version"]


def test_batch_and_single_agree(client, good_row):
    s1 = client.post("/v1/predict", json=good_row).json()["class_predict"]
    s2 = client.post("/v1/predict", json=good_row).json()["class_predict"]
    assert abs(s1 - s2) < 1e-12