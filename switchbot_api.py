#!/usr/bin/env python3

import time
import hashlib
import hmac
import base64
import uuid
import sys
import requests
import json

def make_secret(secret_key):
    # クライアントシークレットキーをbytes列に変換
    return bytes(secret_key, 'utf-8')

def make_sign(secret_key, token, t, nonce):
    # 署名を作成
    string_to_sign = f'{token}{t}{nonce}'
    string_to_sign = bytes(string_to_sign, 'utf-8')
    sign = base64.b64encode(hmac.new(secret_key, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign

def make_t():
    # 現在のタイムスタンプをミリ秒で取得
    return str(int(round(time.time() * 1000)))

def make_nonce():
    # UUIDを生成
    return str(uuid.uuid4())

def get_device_status(token, secret_key, device_id):
    # デバイスのステータスを取得
    secret_key = make_secret(secret_key)
    t = make_t()
    nonce = make_nonce()
    sign = make_sign(secret_key, token, t, nonce)

    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/status"
    headers = {
        "Authorization": token,
        "sign": sign,
        "t": t,
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    # コマンドライン引数の数をチェック
    if len(sys.argv) != 4:
        print("Usage: python switchbot_api.py <token> <secret_key> <device_id>")
        sys.exit(1)

    token = sys.argv[1]
    secret_key = sys.argv[2]
    device_id = sys.argv[3]

    # デバイスのステータスを取得して表示
    data = get_device_status(token, secret_key, device_id)
    print(json.dumps(data, indent=2))
