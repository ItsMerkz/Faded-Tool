import tls_client
import pystyle 
from pystyle import Colorate, Colors
import random 
from veilcord import VeilCord
from captchatools import new_harvester
from Modules import captcha 
import requests 
import json 
import websocket 
import time 
from websocket import WebSocket
from Modules import misc
import string 

def ChangeNickname(token: str, serverid: int, nickname):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-GB',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'cookie': '__dcfduid=23a63d20476c11ec9811c1e6024b99d9; __sdcfduid=23a63d21476c11ec9811c1e6024b99d9e7175a1ac31a8c5e4152455c5056eff033528243e185c5a85202515edb6d57b0; locale=en-GB',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMS45Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTc3NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM1NTQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
            'te': 'trailers'
        }

        if misc.config["Advanced"]["tls_client"]:
            if misc.config["Proxy"]["Use_Proxy"]:
                with open("Input/proxies.txt", "r") as f:
                    proxy = "http://" + random.choice(f.readlines()).strip()
            else:
                proxy = None
            resp = misc.client.patch(f"https://discord.com/api/v9/guilds/{serverid}/members/@me", headers=headers, proxy=proxy, json={
                    "nick": nickname
                })
        else:
            resp = misc.client.patch(f"https://discord.com/api/v9/guilds/{serverid}/members/@me", headers=headers, json={
                "nick": nickname
                })
        if resp.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{resp.status_code}] Changed Nickname {tucan}", True))
        elif resp.status_code in [400, 401, 403]:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{resp.status_code}] Failed Changing Nickname {tucan}", True))
        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{resp.status_code}] Error Occurred {tucan}", True))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def Boost(token: str, serverid: int):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

        response = misc.client.get("https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={"Authorization": token})
        if response.status_code in [403, 401]:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] {tucan} Does Not Have Nitro", True))
        else:
            for sub in response.json():
                misc.subs_id.append(sub["id"])

            for i in range(len(misc.subs_id)):
                resp = misc.client.put(f"https://discord.com/api/v9/guilds/{serverid}/premium/subscriptions", headers={"Authorization": token}, json={
                    "user_premium_guild_subscription_slot_ids": [f"{misc.subs_id[i]}"]
                })
                if resp.status_code in  [200, 201, 203, 204]:
                    print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{resp.status_code}] Boosted Server Successfully {tucan}"))
                elif resp.status_code == 400:
                    print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{resp.status_code}] Failed To Boost {tucan}"))
                else:
                    print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{resp.status_code}] Error Occurred {tucan}"))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def BypassMembershipScreening(token: str, serverid):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-GB',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'cookie': '__dcfduid=23a63d20476c11ec9811c1e6024b99d9; __sdcfduid=23a63d21476c11ec9811c1e6024b99d9e7175a1ac31a8c5e4152455c5056eff033528243e185c5a85202515edb6d57b0; locale=en-GB',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMS45Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTc3NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM1NTQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
            'te': 'trailers'
        }
        if misc.config["Proxy"]["Use_Proxy"]:
            with open("Input/proxies.txt", "r") as f:
                proxy = "http://" + random.choice(f.readlines()).strip()
        else:
            proxy = None

        response = misc.client.get(f"https://discord.com/api/v9/guilds/{serverid}/member-verification", headers=headers, proxy=proxy)
        if "version" in response.text:
            resp = misc.client.put(f"https://discord.com/api/v9/guilds/{serverid}/requests/@me", headers=headers, json=response.json(), proxy=proxy)
            if resp.status_code in [200, 201, 204]:
                if resp.json()["application_status"]:
                    print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{resp.status_code}] Bypassed Membership Screening {tucan}"))
                elif resp.json()["message"] == "This user is already a member, join request is already closed":
                    print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{resp.status_code}] Already Bypassed Membership Screening {tucan}"))
                else:
                    print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{resp.status_code}] Failed Bypassed Membership Screening {tucan}"))
            else:
                print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{resp.status_code}] Failed Bypassed Membership Screening {tucan}"))
        else:
            print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{response.status_code}] No Membership Screening Detected {tucan}"))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def Join(invite: str, token: str, boost, nickname):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "Authorization": token,
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9013 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "America/New_York",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDEzIiwib3NfdmVyc2lvbiI6IjEwLjAuMjI2MjEiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTMgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMiBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMjIuMy4yIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTk5NTM3LCJuYXRpdmVfYnVpbGRfbnVtYmVyIjozMjI2NiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==",
        }

        if misc.config["Advanced"]["tls_client"]:
            if not misc.config["Proxy"]["Use_Proxy"]:
                proxy = None
            else:
                with open("Input/proxies.txt", "r") as f:
                    proxi = random.choice(f.readlines()).strip()
                    proxy = "http://" + proxi 

            session_id = ''.join(random.choice(string.ascii_lowercase) + random.choice(string.digits) for _ in range(16))
            res = misc.client.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                'session_id': session_id
            }, proxy=proxy)
        else:
            session_id = ''.join(random.choice(string.ascii_lowercase) + random.choice(string.digits) for _ in range(16))
            res = misc.client.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                'session_id': session_id
            })
        if misc.config["Developer"]["debug"]:
            print(res.text)
        else:
            pass
        if res.status_code == 400:
            sitekey = res.json()["captcha_sitekey"]
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [400] Captcha Required ({sitekey})", True))
        elif res.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{res.status_code}] Joined ({invite}) {tucan}", True))
            if nickname != None:
                ChangeNickname(token, res.json()["guild"]["id"], nickname)
            else:
                pass
            if boost:
                Boost(token, res.json()["guild"]["id"])
            else:
                pass
            if misc.config["Guild"]["bypass_membership_screening"]:
                BypassMembershipScreening(token, res.json()["guild"]["id"])
            else:
                pass
        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{res.status_code}] Unknown Error Occurred", True))

        if res.status_code == 400:
            if misc.config["Captcha"]["Api"] == 1:
                solvingsite = "Capmonster"
            elif misc.config["Captcha"]["Api"] == 2:
                solvingsite = "Anticaptcha"
            elif misc.config["Captcha"]["Api"] == 3:
                solvingsite = "2Captcha"
            elif misc.config["Captcha"]["Api"] == 4:
                pass
            elif misc.config["Captcha"]["Api"] == 5:
                pass

            if misc.config["Captcha"]["Api"] != 4 and misc.config["Captcha"]["Api"] != 5:
                harvester = new_harvester(
                    api_key=misc.config["Captcha"]["Captcha_key"],
                    solving_site=solvingsite,
                    captcha_type="hcaptcha",
                    sitekey=sitekey,
                    captcha_url="https://discord.com/")
                answer = harvester.get_token()
            elif misc.config["Captcha"]["Api"] == 4:
                answer = captcha.Capsolver(misc.config["Captcha"]["Captcha_key"]).GetSolution(captcha.Capsolver(misc.config["Captcha"]["Captcha_key"]).CreateTask(res.json()["captcha_rqtoken"], sitekey, f"http:{proxi}"))
            elif misc.config["Captcha"]["Api"] == 5:
                answer = captcha.Hcoptcha(misc.config["Captcha"]["Captcha_key"]).Solve(res.json()["captcha_rqtoken"], sitekey, f"{proxi}")

            if misc.config["Advanced"]["tls_client"]:
                if misc.config["Proxy"]["Use_Proxy"]:
                    with open("Input/proxies.txt", "r") as f:
                        proxy = "http://" + random.choice(f.readlines()).strip()
                else:
                    proxy = None

                session_id = ''.join(random.choice(string.ascii_lowercase) + random.choice(string.digits) for _ in range(16))

                headers = {
                    "authority": "discord.com",
                    "accept": "*/*",
                    "accept-language": "en-US",
                    "connection": "keep-alive",
                    "Authorization": token,
                    "content-type": "application/json",
                    "origin": "https://discord.com",
                    "referer": "https://discord.com/channels/@me",
                    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9013 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36",
                    "x-debug-options": "bugReporterEnabled",
                    "x-captcha-key": answer,
                    "x-captcha-rqtoken": res.json()["captcha_rqtoken"],
                    "x-discord-locale": "en-US",
                    "x-discord-timezone": "America/New_York",
                    "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDEzIiwib3NfdmVyc2lvbiI6IjEwLjAuMjI2MjEiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTMgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMiBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMjIuMy4yIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTk5NTM3LCJuYXRpdmVfYnVpbGRfbnVtYmVyIjozMjI2NiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==",
                }
                resp = misc.client.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, proxy=proxy, json={
                    'session_id': session_id,
                })
            else:
                session_id = ''.join(random.choice(string.ascii_lowercase) + random.choice(string.digits) for _ in range(16))
                resp = misc.client.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                    'session_id': session_id,
                })
            if resp.status_code in [200, 201, 204]:
                print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{resp.status_code}] Joined ({invite}) {tucan}", True))
                if nickname != None:
                    ChangeNickname(token, resp.json()["guild"]["id"], nickname)
                else:
                    pass
                if boost:
                    Boost(token, resp.json()["guild"]["id"])
                else:
                    pass
                if misc.config["Guild"]["bypass_membership_screening"]:
                    BypassMembershipScreening(token, resp.json()["guild"]["id"])
            elif resp.status_code == 400:
                print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{resp.status_code}] Captcha Invalid ({invite}) {tucan}", True))
                # Join(invite, token, boost, nickname)
            elif resp.status_code == 429:
                print(Colorate.Horizontal((Colors.red_to_yellow, f"(*) [{resp.status_code}] Ratelimited {tucan}")))

            else:
                print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{resp.status_code}] Unknown Error Occurred {tucan}", True))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [RET] Retrying..."))
        Join(invite, token, boost, nickname)

def Leaver(token: str, serverid: int):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token
        if misc.config["Proxy"]["Use_Proxy"]:
            with open("Input/proxies.txt", "r") as f:
                proxy = "http://" + random.choice(f.readlines()).strip()
        else:
            proxy = None

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'X-Context-Properties': 'eyJsb2NhdGlvbiI6Ikludml0ZSBCdXR0b24gRW1iZWQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6bnVsbCwibG9jYXRpb25fY2hhbm5lbF9pZCI6IjExMzczODQwOTM1Njc0MzQ4MTQiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjEsImxvY2F0aW9uX21lc3NhZ2VfaWQiOiIxMTM3NDExODAxMTM1NDU2MzY3In0=',
            'Authorization': 'OTY1NDM1OTM2ODQ0NDMxMzcw.GfKwMA.VUHWIPgIV4rDJBB9jU7hJicpIInRv3WVGI51LM',
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExNi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE2LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjE4MDUxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'Europe/London',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'Alt-Used': 'discord.com',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/channels/^@me/1137384093567434814',
            # 'Cookie': '__dcfduid=036331501c3911ee9218eb7ee11f2772; __sdcfduid=036331511c3911ee9218eb7ee11f27724f6f628decef1de81d33835aae31e99100eea37707b29c3dc8c1cf572c5cc5ec; OptanonConsent=isIABGlobal=false&datestamp=Sat+Aug+05+2023+11^%^3A06^%^3A48+GMT^%^2B0100+(British+Summer+Time)&version=6.33.0&hosts=&landingPath=https^%^3A^%^2F^%^2Fdiscord.com^%^2F&groups=C0001^%^3A1^%^2CC0002^%^3A0^%^2CC0003^%^3A0; __stripe_mid=79ace875-842e-47f9-b0b5-af094fe94debcd1cff; _ga=GA1.2.2099359268.1690645385; cf_clearance=o1XI.JYYWrCu25C882dONrJmqFbQKyUkMXObxYCP1Po-1691250488-0-1-2404c209.62f6736d.7481a190-0.2.1691250488; __cfruid=2297b08ef3cfd0cb40b544e3a8ce0e3b2fe69acd-1691245372; locale=en-US',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        resp = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{serverid}", headers=headers, json={"lurking": False})
        if resp.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{resp.status_code}] Left {tucan}", True))
        elif resp.status_code in [400, 404]:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{resp.status_code}] Not In Server {tucan}"))
        elif resp.status_code == 429:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [429] Ratelimited"))
        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{resp.status_code}] Failed Leaving {tucan}", True))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def CancelBoosts(token: str):
        try:
            response = misc.client.get("https://discord.com/api/v9/users/@me/guilds", headers={"Authorization": token})
            for guild in response.json():
                data = open("Input/serverids.txt")
                if guild['id'] not in data.read():
                    print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{response.status_code}] Saving ServerID To File"))
                    with open("Input/serverids.txt", "a") as f:
                        f.write(f"{guild['id']}\n")
                        f.close()
                else:
                    print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] ServerID Already In File"))
        except Exception as err:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def SendChannelMessage(token: str, channelid: int, message: str):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/104.0',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Content-Type': 'application/json',
            'Authorization': token,
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwOS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA5LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTczNzY3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9',
            'X-Discord-Locale': 'en-US',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'Alt-Used': 'discord.com',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/channels/@me',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        # content = json.load(open("Input/message.json", encoding="utf-8", errors="ignore"))
        # message = content["content"]

        if misc.config["Advanced"]["tls_client"]:
            if misc.config["Proxy"]["Use_Proxy"] != True:
                proxy = None 
            else:
                with open("Input/proxies.txt", "r") as f:
                    proxi = random.choice(f.readlines()).strip()
                    proxy = "http://" + proxi 
            
            response = misc.client.post(f"https://discord.com/api/v9/channels/{channelid}/messages", headers=headers, proxy=proxy, json={
                "content": message,
                "nonce": misc.Utils.nonce(),
                "tts": False  
            })
        else:
            response = misc.client.post(f"https://discord.com/api/v9/channels/{channelid}/messages", headers=headers, json={
                "content": message,
                "nonce": misc.nonce(),
                "tts": False  
            })
        if response.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{response.status_code}] Sent Message ({channelid}) {tucan}"))
        elif response.status_code in [404] and "message" in response.text:
            if response.json()["message"] == "Unknown Message":
                print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Error Sending Message (Unknown Message) {tucan}"))
        elif response.status_code == 400 and "captcha_key" in response.text:
            sitekey = response.json()["captcha_sitekey"]
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Captcha Required ({sitekey}) {tucan}"))
            # TODO: add capmonster_python module for capmonster users, requires rq_data for sending dm captcha!
            if misc.config["Advanced"]["tls_client"]:
                if not misc.config["Proxy"]["Use_Proxy"]:
                    proxy = None 
                else:
                    with open("Input/proxies.txt", "r") as f:
                        proxy = "http://" + random.choice(f.readlines()).strip()
                        if misc.config["Captcha"]["Api"] == 2:
                            solvingsite = "Anticaptcha"
                        elif misc.config["Captcha"]["Api"] == 3:
                            solvingsite = "2Captcha"
                        elif misc.config["Captcha"]["Api"] == 4:
                            solvingsite = "capsolver"
                        
                        if misc.config["Captcha"]["Api"] != 4:
                            harvester = new_harvester(
                                api_key=misc.config["Captcha"]["Captcha_key"],
                                solving_site=solvingsite,
                                captcha_type="hcaptcha",
                                sitekey=sitekey,
                                captcha_url="https://discord.com/")
                            answer = harvester.get_token()
                        else:
                            answer = captcha.Capsolver(misc.config["Captcha"]["Captcha_key"]).GetSolution(captcha.Capsolver(misc.config["Captcha"]["Captcha_key"]).CreateTask(None, sitekey, proxi))

                resp = misc.client.post(f"https://discord.com/api/v9/channels/{channelid}/messages", headers=headers, proxy=proxy, json={
                    "captcha_key": answer,
                    "captcha_rqtoken": response.json()["captcha_rqtoken"],
                    "content": message,
                    "nonce": misc.nonce(),
                    "tts": False
                })
            else:
                resp = misc.client.post(f"https://discord.com/api/v9/channels/{channelid}/messages", headers=headers, json={
                    "captcha_key": answer,
                    "captcha_rqtoken": response.json()["captcha_rqtoken"],
                    "content": message,
                    "nonce": misc.nonce(),
                    "tts": False
                })
            if resp.status_code == 400 and "captcha_key" in resp.text:
                print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{resp.status_code}] Failed Solving Captcha ({channelid}) {tucan}"))

            elif resp.status_code == 403 and "message" in response.text:
                print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{resp.status_code}] Cannot Send Messages To {channelid}"))
        # elif response.status_code == 429:
        #     print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Ratelimited"))
            else:
                print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{resp.status_code}] {resp.text}"))

        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{response.status_code}] Failed Sending "))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def VcSpammer(token: str, guildid, channelid):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

        ws = WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
        hello = json.loads(ws.recv())
        heartbeat_interval = hello['d']['heartbeat_interval']
        ws.send(json.dumps({"op": 2,"d": {"token": token,"properties": {"$os": "windows","$browser": "Discord","$device": "desktop"}}}))
        ws.send(json.dumps({"op": 4,"d": {"guild_id": guildid,"channel_id": channelid,"self_mute": False,"self_deaf": False}}))
        print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [200] Joined VC {tucan}"))
        for i in range(random.randint(1, 10000)):
            time.sleep(1)
            ws.send(json.dumps({"op": 4,"d": {"guild_id": guildid,"channel_id": channelid,"self_mute": random.choice([True, False]),"self_deaf": random.choice([True, False])}}))
        ws.send(json.dumps({"op": 18,"d": {"type": "guild","guild_id": guildid,"channel_id": channelid,"preferred_region": "europe"}}))
        print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [200] Joined VC {tucan}"))
        while True:
            time.sleep(heartbeat_interval / 1000)
            try:
                ws.send(json.dumps({"op": 1,"d": None}))
            except Exception:
                break
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))