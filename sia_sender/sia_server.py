import json
from flask import Flask, request
from pysiaalarm import SIAClient

app = Flask(__name__)

OPTIONS_PATH = "/data/options.json"

def load_options():
    with open(OPTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

opts = load_options()

SIA_ACCOUNT = opts.get("account")
SIA_KEY = opts.get("key")
SIA_HOST = opts.get("host")
SIA_PORT = int(opts.get("port"))

client = SIAClient(SIA_ACCOUNT, SIA_KEY, SIA_HOST, SIA_PORT)

@app.route("/send", methods=["POST"])
def send_sia():
    data = request.json or {}
    event = data.get("event")
    zone = data.get("zone", "01")

    mapping = {
        "ALARM": "BA",
        "DISARM": "CL",
        "ARM": "OP",
        "TAMPER": "TA",
    }

    sia_event = mapping.get(event, "BA")

    msg = client.create_event(sia_event, zone)
    client.send(msg)

    return {"status": "sent", "sia_event": sia_event, "zone": zone}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8127)
