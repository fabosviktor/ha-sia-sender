import json
from flask import Flask, request
from pysiaalarm import SIAClient, SIAAccount

app = Flask(__name__)

OPTIONS_PATH = "/data/options.json"

def load_options():
    with open(OPTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

opts = load_options()

SIA_ACCOUNT = opts.get("account")
SIA_KEY = opts.get("key") or ""   # 🔧 üres kulcs, ha nem kell
SIA_HOST = opts.get("host")
SIA_PORT = int(opts.get("port"))

accounts = [SIAAccount(SIA_ACCOUNT, SIA_KEY)]

client = SIAClient(SIA_HOST, SIA_PORT, accounts)
