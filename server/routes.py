from re import sub
from flask import request
from server import app
import subprocess


@app.post("/command")
def command():
    """ Execute the command and return the output """
    if missingParams := missing(request, data=["command"]):
        return {"error": missingParams}, 400
    command = request.json["command"]
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = process.communicate()[0]
    return {"stdout": stdout.decode("utf-8")}

@app.post("/dummy")
def dummy():
    """ Dummy function for testing """
    if missingParams := missing(request, data=["input"]):
        return {"error": missingParams}, 400
    if request.json["input"] == "valid input :)":
        return {"success": "nice input bro"}, 200
    else:
        return {"error": "bad input"}, 400

def missing(request, data=None):
    """ Return error message about missing paramaters if there are any """
    missingData = []
    if data:
        for field in data:
            if field not in request.json:
                missingData.append(field)
    if not missingData:
        return None
    errMsg = "request is missing the following parameters: "
    if missingData:
        errMsg += "data=['"
        errMsg += "', '".join(missingData)
        errMsg += "']"
    return errMsg