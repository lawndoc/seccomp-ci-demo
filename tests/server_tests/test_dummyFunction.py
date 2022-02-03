import json


def testDummyFunction(client):
    response = client.post("/dummy",
                           headers={"Content-Type": "application/json"},
                           data=json.dumps({"input": "valid input :)"}))
    assert response.status_code == 200
    assert response.json["success"] == "nice input bro"

def testBadInputDummyFunction(client):
    response = client.post("/dummy",
                           headers={"Content-Type": "application/json"},
                           data=json.dumps({"input": "bad input :("}))
    assert response.status_code == 400
    assert response.json["error"] == "bad input"

def testMissingInputDummyFunction(client):
    response = client.post("/dummy",
                           headers={"Content-Type": "application/json"},
                           data=json.dumps({}))
    assert response.status_code == 400
    assert response.json["error"] == "request is missing the following parameters: data=['input']"
