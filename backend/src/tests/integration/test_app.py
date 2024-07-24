def test_status(client):
    response = client.get("/health_check")
    result = response.json()
    assert result is not None
    assert "message" in result
    assert result["message"] == "OK"
