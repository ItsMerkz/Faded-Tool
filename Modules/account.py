from Modules import misc
import pystyle
from pystyle import Colorate, Colors
import datetime 
import random 
import os 
import base64
from Modules import captcha 
from captchatools import new_harvester

def Check(token: str):
    try:
        if ':' in token:
            tken = token.split(":")[2]
            email = token.split(":")[0]
            pass_word = token.split(":")[1]
            token = f'{email}:{pass_word}:{tken}'
        else:
            token, tken = token

        if misc.config["General"]["hide_token"]:
            tucan = tken[:39] + "***************************************"
        else:
            tucan = tken

        validated = open("Input/valid.txt").read()
        locked_token = open("Input/locked.txt").read()
        invalidated = open("Input/Invalid.txt").read()

        res = misc.client.get("https://discord.com/api/v9/users/@me/affinities/guilds", headers={
            "Authorization": tken
        })
        if res.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) {tucan} Valid", True))
            if token in validated:
                pass
            else:
                with open("Input/Valid.txt", "a") as f:
                    f.write(f"{token}\n")
                    f.close()
        elif res.status_code == 401:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) {tucan} Invalid", True))
            if token in invalidated:
                pass
            else:
                with open("Input/Invalid.txt", "a") as f:
                    f.write(f"{token}\n")
                    f.close()
        elif res.status_code == 403:
            print(Colorate.Horizontal(Colors.purple_to_red, f"(*) {tucan} Locked", True))
            if token in locked_token:
                pass
            else:
                with open("Input/Locked.txt", "a") as f:
                    f.write(f"{token}\n")
                    f.close()
        else:
            print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) {tucan} Error", True))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def NitroCheck(token: str):
    try:
        now = datetime.now()
        now = str(now)
        if ":" in token:
            email = token.split(":")[0]
            pass_word = token.split(":")[1]
            token = token.split(":")[2]
            tken = f"{email}:{pass_word}:{token}"
        else:
            tken = token

        if "\n" in token:
            token = token.split("\n")[0]
        else:
            token = token

        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "***************************************"
        else:
            tucan = token

        response = misc.client.get("https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={"Authorization": token})
        if misc.config["Developer"]["debug"]:
            if "id" in response.text:
                cooldown = response.json()[0]["cooldown_ends_at"]
                print(Colorate.Horizontal(Colors.blue_to_purple, f"(*) [DEBUG] {response.status_code} | {cooldown} {tucan}"))
            else:
                print(Colorate.Horizontal(Colors.blue_to_purple, f"(*) [{response.status_code}] Does Not Have Nitro {tucan}"))
        else:
            if response.status_code in [401, 403]:
                print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Token Does Not Have Nitro {tucan}"))
            elif "premium_guild_subscription" in response.json():
                print(Colorate.Horizontal(Colors.red_to_purple, f"(*) {response.status_code}] Token Does Not Have Nitro Boosts {tucan}"))

            else:
                if response.json()[0]["premium_guild_subscription"] or response.json()[1]["premium_guild_subscription"]:
                    if now > response.json()[0]["cooldown_ends_at"]:
                        print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{response.status_code}] Token Cooldown Ended {tucan}"))
                        with open("Output/tokens.txt", "a") as f:
                            f.write(f"{tken}\n")
                            f.close()
                    else:
                        print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Used {tucan}"))
                        with open("Output/used.txt", "a") as f:
                            f.write(f"{tken}\n")
                            f.close()
                elif response.json()[0]["premium_guild_subscription"] or response.json()[1]["premium_guild_subscription"] != True:
                    print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{response.status_code}] Unused {tucan}"))
                    with open("Output/tokens.txt", "a") as f:
                        f.write(f"{tken}\n")
                        f.close()
                else:
                    print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{response.status_code}] Error Occured | {response.text}"))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def ChangeBio(token: str):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

        with open("Input/bios.txt", "r") as f:
            bio = random.choice(f.readlines()).strip()

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
        if misc.config["Advanced"]["tls_client"]:
            if misc.config["Proxy"]["Use_Proxy"] != True:
                proxy = None
            else:
                with open("Input/proxies.txt", "r") as f:
                    proxy = "http://" + random.choice(f.readlines()).strip()

            response = misc.client.patch("https://discord.com/api/v9/users/@me/profile", headers=headers, proxy=proxy, json={
                "bio": bio
            })
        else:
            response = misc.client.patch("https://discord.com/api/v9/users/@me/profile", headers=headers, json={
                "bio": bio
            })
        if response.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{response.status_code}] Changed Bio Successfully {tucan}"))
        elif response.status_code in [400, 401, 403]:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Failed To Change Bio {tucan}"))
        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{response.status_code}] Error Occurred Changing Bio {tucan}"))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def ChangePassword(token: str, new_password: str):
    try:
        password = token.split(":")[1]
        email = token.split(":")[0]
        token = token.split(":")[2]

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
        if misc.config["Advanced"]["tls_client"]:
            if misc.config["Proxy"]["Use_Proxy"] != True:
                proxy = None
            else:
                with open("Input/proxies.txt", "r") as f:
                    proxy = "http://" + random.choice(f.readlines()).strip()
            response = misc.client.patch("https://discord.com/api/v9/users/@me", headers=headers, proxy=proxy, json={
                "password": password,
                "new_password": new_password
            })
        else:
            response = misc.client.patch("https://discord.com/api/v9/users/@me", headers=headers, json={
                "password": password,
                "new_password": new_password
            })
        if response.status_code in [200, 201, 204]:
            token = response.json()["token"]
            if misc.config["General"]["hide_token"]:
                tucan = token[:39] + "********************"
            else:
                tucan = token
            print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{response.status_code}] Changed Password {tucan}"))
            with open("Output/tokens.txt", "a") as f:
                token = response.json()["token"]
                f.write(f"{email}:{new_password}:{token}\n")
                f.close()
        elif response.status_code in [400, 401, 403]:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Failed Changing Password {tucan} | {response.text}"))
        elif response.status_code == 429:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Ratelimited"))
        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{response.status_code}] {response.text}"))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def ChangePfp(token: str):
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

        a = random.choice(os.listdir("Input/Avatars/"))
        avatar = folder='\\'+a
        image = base64.b64encode(open(f"{avatar}", "rb").read()).decode('ascii')
    
        response = misc.client.patch("https://discord.com/api/v9/users/@me", headers=headers, json={
            "avatar": f"data:image/png;base64,{image}"
        })

        if response.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.yellow_to_green, f"(*) [{response.status_code}] Changed Pfp {tucan}"))
        elif response.status_code in [400, 404]:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Error Encoding B64 String {tucan}"))
        elif response.status_code in [429]:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Ratelimited"))
        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{response.status_code}] An Error Occurred {response.text}"))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def SendFriendRequest(token: str, friendid):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Referer': 'https://discord.com/channels/^@me',
            'X-Context-Properties': 'eyJsb2NhdGlvbiI6IkNvbnRleHRNZW51In0=',
            'Authorization': token,
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExNS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE1LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjE3NDM2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'Europe/London',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'Alt-Used': 'discord.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

        if misc.config["Advanced"]["tls_client"]:
            if not misc.config["Proxy"]["Use_Proxy"]:
                proxy = None 
            else:
                with open("Input/proxies.txt", "r") as f:
                    proxi = random.choice(f.readlines()).strip()
                    proxy = "http://" + proxi 

            response = misc.client.put(f"https://discord.com/api/v9/users/@me/relationships/{friendid}", headers=headers, proxy=proxy, json={})
        else:
            response = misc.client.put(f"https://discord.com/api/v9/users/@me/relationships/{friendid}", headers=headers, json={})    

        if response.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{response.status_code}] Sent Friend Request {tucan}"))
        elif response.status_code in [400]:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Captcha Required "))
            if misc.config["User"]["solvecaptcha_on_friendreq"]:

                if misc.config["Captcha"]["Api"] == 1:
                    solvingsite = "Capmonster"
                elif misc.config["Captcha"]["Api"] == 2:
                    solvingsite = "Anticaptcha"
                elif misc.config["Captcha"]["Api"] == 3:
                    solvingsite = "2Captcha"
                elif misc.config["Captcha"]["Api"] == 4:
                    pass

                if misc.config["Captcha"]["Api"] != 4:
                    harvester = new_harvester(
                        api_key = misc.config["Captcha"]["Captcha_key"],
                        solving_site = solvingsite,
                        captcha_type = "hcaptcha",
                        sitekey = response.json()["captcha_sitekey"],
                        captcha_url = "https://discord.com/")
                    answer = harvester.get_token()
                else:
                    answer = captcha.Capsolver(misc.config["Captcha"]["Captcha_key"]).GetSolution(captcha.Capsolver(misc.config["Captcha"]["Captcha_key"]).CreateTask(None, response.json()["captcha_sitekey"], proxi))

                if misc.config["Advanced"]["tls_client"]:
                    if not misc.config["Proxy"]["Use_Proxy"]:
                        proxy = None 
                    else:
                        with open("Input/proxies.txt", "r") as f:
                            proxy = "http://" + random.choice(f.readlines()).strip()

                    resp = misc.client.put(f"https://discord.com/api/v9/users/@me/relationships/{friendid}", headers=headers, proxy=proxy, json={
                        "captcha_key": answer
                    })
                else:
                    resp = misc.client.put(f"https://discord.com/api/v9/users/@me/relationships/{friendid}", headers=headers, json={
                        "captcha_key": answer
                    }) 
                if resp.status_code in [200, 201, 204]:
                    print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{resp.status_code}] Sent Friend Request {tucan}"))
                else:
                    print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{resp.status_code}] Failed Sending Friend Request {tucan}"))
            else:
                pass
        elif response.status_code == 429:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"(*) [{response.status_code}] Ratelimited {tucan}"))
        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{response.status_code}] An Error Occurred {tucan}"))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def UsernameChanger(token: str, password: str, username: str):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Content-Type': 'application/json',
            'Authorization': token,
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExMS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTExLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTg1NTE2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9',
            'X-Discord-Locale': 'en-US',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'Alt-Used': 'discord.com',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/channels/@me',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        if misc.config["Advanced"]["tls_client"]:
            if misc.config["Proxy"]["Use_Proxy"] != True:
                proxy = None 
            else:
                with open("Input/proxies.txt", "r") as f:
                    proxy = "http://" + random.choice(f.readlines()).strip()
            
            response = misc.client.patch("https://discord.com/api/v9/users/@me", headers=headers, proxy=proxy, json={
                "password": password, 
                "username": username 
            })
        else:
            response = misc.client.patch("https://discord.com/api/v9/users/@me", headers=headers, json={
                "password": password, 
                "username": username
            })
        if response.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{response.status_code}] Changed Username For {tucan}"))
        elif response.status_code in [400]:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{response.status_code}] Bad Request (Password Incorrect) {tucan}"))
        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{response.status_code}] Error Occured {tucan}"))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))
        
def HouseChanger(token: str):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Content-Type': 'application/json',
            'Authorization': token,
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExMS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTExLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTg1NTE2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9',
            'X-Discord-Locale': 'en-US',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'Alt-Used': 'discord.com',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/channels/@me',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        if misc.config["Advanced"]["tls_client"]:
            if misc.config["Proxy"]["Use_Proxy"] != True:
                proxy = None 
            else:
                with open("Input/proxies.txt", "r") as f:
                    proxy = "http://" + random.choice(f.readlines()).strip()

            response = misc.client.post("https://discord.com/api/v9/hypesquad/online", headers=headers, proxy=proxy, json={
                "house_id": random.randint(1, 3)
            })
        else:
            response = misc.client.post("https://discord.com/api/v9/hypesquad/online", headers=headers, json={
                "house_id": random.randint(1, 3)
            })
        
        if response.status_code in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.green_to_yellow, f"(*) [{response.status_code}] Changed Hypesquad {tucan}"))
        else:
            print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [{response.status_code}] An Error Occurred {tucan}"))
    except Exception as err:
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) [ERR] {err}"))

def mailverify(token: str):
    try:
        if misc.config["General"]["hide_token"]:
            tucan = token[:39] + "********************"
        else:
            tucan = token

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
                'Accept': '*/*',
                'Accept-Language': 'en-GB,en;q=0.5',
                'Content-Type': 'application/json',
                'Authorization': token,
                'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExNi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE2LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjE4NjA0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
                'X-Discord-Locale': 'en-GB',
                'X-Discord-Timezone': 'Europe/London',
                'X-Debug-Options': 'bugReporterEnabled',
                'Origin': 'https://discord.com',
                'Alt-Used': 'discord.com',
                'Connection': 'keep-alive',
                'Referer': 'https://discord.com/channels/^@me',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            }

            if misc.config["Advanced"]["tls_client"]:
                if misc.config["Proxy"]["Use_Proxy"] != True:
                    proxy = None 
                else:
                    with open("Input/proxies.txt", "r") as f:
                        proxy = "http://" + random.choice(f.readlines()).strip()

                response = misc.client.post("https://discord.com/api/v9/users/@me", headers=headers, proxy=proxy, json={
                    "email": "",
                    "password": ""
                })
    
    except Exception as err:
        print(err)