import json 
import tls_client
import httpx 
import random 
import time 
import datetime 
import pystyle 
from pystyle import Colorate, Colors 
config = json.load(open("Storage/settings.json", encoding="utf-8"))
subs_id = []

# Configuration for tls / httpx client
if config["Proxy"]["Use_Proxy"] != True:
    proxy = None
elif config["Proxy"]["Use_Proxy"]:
    with open("Input/proxies.txt", "r") as f:
        proxy = "http://" + random.choice(f.readlines()).strip()

if config["Advanced"]["tls_client"]:
    client = tls_client.Session(
        client_identifier="discord_1_0_9013",
        h2_settings={
            "HEADER_TABLE_SIZE": 65536,
            "MAX_CONCURRENT_STREAMS": 1000,
            "INITIAL_WINDOW_SIZE": 6291456,
            "MAX_HEADER_LIST_SIZE": 262144
        },
        h2_settings_order=[
            "HEADER_TABLE_SIZE",
            "MAX_CONCURRENT_STREAMS",
            "INITIAL_WINDOW_SIZE",
            "MAX_HEADER_LIST_SIZE"

        ],
        supported_signature_algorithms=[
            "ECDSAWithP256AndSHA256",
            "PSSWithSHA256",
            "PKCS1WithSHA256",
            "ECDSAWithP384AndSHA384",
            "PSSWithSHA384",
            "PKCS1WithSHA384",
            "PSSWithSHA512",
            "PKCS1WithSHA512",
        ],
        supported_versions=["GREASE", "1.3", "1.2"],
        key_share_curves=["GREASE", "X25519"],
        cert_compression_algo="brotli",
        pseudo_header_order=[
            ":method",
            ":authority",
            ":scheme",
            ":path"

        ],
        connection_flow=15663105,
        header_order=[
            "accept",
            "user-agent",
            "accept-encoding",
            "accept-language"

        ]
    )
else:
    client = httpx.Client(proxies=proxy, timeout=60)

class Utils:
    
    def nonce(self):
        date = datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts)*1000-1420070400000)*4194304)
    

    @staticmethod
    def Format():
        try:
            tokens = open("Input/tokens.txt", "r").readlines()

            for token in tokens:
                tken = token.split(":")[2]
                with open("Output/formatted.txt", "a") as f:
                    f.write(f"{tken}")
                    f.close()
        except Exception as err:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

    @staticmethod
    def ResetFiles():
        try:
            open("Input/tokens.txt", "w").close()
            open("Input/valid.txt", "w").close()
            open("Input/invalid.txt", "w").close()
            open("Input/locked.txt", "w").close()
            open("Input/proxies.txt", "w").close()
            open("Input/bios.txt", "w").close()
            open("Input/serverids.txt", "w").close()
            open("Input/invites.txt", "w").close()
            open("Output/tokens.txt", "w").close()
            open("Output/used.txt", "w").close()
        except Exception as err:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

    @staticmethod
    def ResetConfig():
        try:
            open("Storage/settings.json", "w").close()
            with open("Storage/settings.json", "a") as f:
                f.write("""{
    "Proxy": {
        "Use_Proxy": false
    },
    "Captcha": {
        "Api": 4,
        "Captcha_key": ""
    },
    "General": {
        "hide_token": true
    },
    "Guild": {
        "bypass_membership_screening": true
    },
    "User": {
        "solvecaptcha_on_friendreq": true,
        "friend_delay": true,
        "delay": 10
    },
    "Advanced": {
        "tls_client": true,
        "JA3": ""
    }, 
    "Developer": {
        "debug": false
    }
}""")
                f.close()
        except Exception as err:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))