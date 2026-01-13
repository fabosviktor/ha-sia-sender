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

# -----------------------------
# CRC16-X25 (Enigma II által használt)
# -----------------------------
def crc16_x25(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0x8408
            else:
                crc >>= 1
    crc = ~crc & 0xFFFF
    return crc

# -----------------------------
# SIA-IP DC-09 üzenet küldése
# -----------------------------
def send_sia_event(event_code, zone="01"):
    # SIA DC-09 payload
    payload = f'SIA-DCS"{ACCOUNT}"0000L0#{event_code}{zone}'

    # CRC számítása
    crc_value = crc16_x25(payload.encode("ascii"))
    crc_hex = f"{crc_value:04X}"

    # Teljes SIA-IP üzenet (hossz + payload + CRC)
    full_message = f'{len(payload)} {payload}[{crc_hex}]\r\n'

    print("Küldendő üzenet:", full_message)

    # TCP küldés
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Kapcsolódás sikeres:", HOST, PORT)
            s.sendall(full_message.encode("ascii"))
            print("Üzenet elküldve")
        except Exception as e:
            print("Hiba küldés közben:", e)

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
