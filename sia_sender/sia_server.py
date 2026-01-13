import json
import socket
from flask import Flask, request

app = Flask(__name__)

OPTIONS_PATH = "/data/options.json"

def load_options():
    with open(OPTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

opts = load_options()

ACCOUNT = opts.get("account")
HOST = opts.get("host")
PORT = int(opts.get("port"))

def send_sia_event(event_code, zone="01"):
    # Enigma-kompatibilis SIA DC-09 üzenet
    message = f'SIA-DCS"{ACCOUNT}"0000L0#{event_code}{zone}\r\n'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode("ascii"))

@app.route("/send", methods=["POST"])
def send():
    data = request.json or {}
    event = data.get("event", "ALARM")
    zone = data.get("zone", "01")

    mapping = {
        "ALARM": "BA",
        "DISARM": "CL",
        "ARM": "OP",
        "TAMPER": "TA",
    }

    sia_code = mapping.get(event, "BA")

    send_sia_event(sia_code, zone)

    return {"status": "sent", "event": sia_code, "zone": zone}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8127)
