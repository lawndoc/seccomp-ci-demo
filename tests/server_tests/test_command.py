import json


def testCommand(client):
    response = client.post("/command",
                           headers={"Content-Type": "application/json"},
                           data=json.dumps({"command": "echo test"}))
    assert response.status_code == 200
    assert response.json["stdout"] == "test\n"
    assert response.json["stderr"] == ""

def testMissingInputCommand(client):
    response = client.post("/command",
                           headers={"Content-Type": "application/json"},
                           data=json.dumps({}))
    assert response.status_code == 400
    assert response.json["error"] == "request is missing the following parameters: data=['command']"