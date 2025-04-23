from fastapi.testclient import TestClient
import pytest
from core.dispatcher import app, validate_and_mask_input, process_cli

client = TestClient(app)


def test_rest_success():
    res = client.post("/process", json={"prompt": "こんにちは"})
    assert res.status_code == 200
    assert res.json()["processed_prompt"] == "こんにちは"


def test_rest_bad_request():
    res = client.post("/process", json={"wrong": "data"})
    assert res.status_code == 400


def test_cli_success(runner):
    result = runner.invoke(process_cli, ["hello@example.com"])
    assert result.exit_code == 0
    assert "[EMAIL]" in result.stdout


def test_cli_missing_prompt(runner):
    result = runner.invoke(process_cli, [])
    assert result.exit_code != 0
